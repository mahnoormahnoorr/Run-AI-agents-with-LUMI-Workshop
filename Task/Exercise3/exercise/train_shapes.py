#!/usr/bin/env python3
"""Train a small CNN to recognise shapes (circle, square, cross) in noisy
48x48 images. Synthetic data: no download needed.

It trains correctly and reaches good accuracy. It is also far slower than it
should be. Run with --profile to profile a few steady-state steps.
"""
import argparse
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.profiler import record_function

SIZE = 48


def make_images(n, rng):
    """n noisy images, each with one shape; labels 0=circle, 1=square, 2=cross."""
    yy, xx = np.mgrid[0:SIZE, 0:SIZE]
    labels = rng.integers(0, 3, n)
    cx = rng.uniform(14, 34, n)[:, None, None]
    cy = rng.uniform(14, 34, n)[:, None, None]
    r = rng.uniform(6, 12, n)[:, None, None]
    circle = (xx - cx) ** 2 + (yy - cy) ** 2 <= r ** 2
    square = (np.abs(xx - cx) <= 0.8 * r) & (np.abs(yy - cy) <= 0.8 * r)
    cross = ((np.abs(xx - cx) <= r) & (np.abs(yy - cy) <= r / 4)) | \
            ((np.abs(yy - cy) <= r) & (np.abs(xx - cx) <= r / 4))
    lab = labels[:, None, None]
    img = np.where(lab == 0, circle, np.where(lab == 1, square, cross)).astype(np.float64)
    img += rng.normal(0, 0.3, img.shape)
    return img[:, None], labels


def augment(batch, rng):
    """Random flips and a little extra pixel noise, sample by sample."""
    out = np.empty_like(batch)
    for i in range(batch.shape[0]):
        img = batch[i, 0]
        if rng.random() < 0.5:
            img = img[:, ::-1]
        if rng.random() < 0.5:
            img = img[::-1, :]
        for y in range(SIZE):
            for x in range(SIZE):
                out[i, 0, y, x] = img[y, x] + rng.normal(0, 0.1)
    return out


class ShapeNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.fc1 = nn.Linear(32 * 12 * 12, 64)
        self.fc2 = nn.Linear(64, 3)

    def forward(self, x):
        mean = torch.tensor([0.25]).to(x.device)
        x = (x - mean) / 0.5
        # TODO: the convolutions are probably the slow part -- optimise these first
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        return self.fc2(F.relu(self.fc1(x.flatten(1))))


def accuracy(model, X, y, device):
    model.eval()
    correct = 0
    with torch.no_grad():
        for i in range(0, len(X), 16):
            xb = torch.tensor(X[i:i + 16], dtype=torch.float32).to(device)
            yb = torch.tensor(y[i:i + 16]).to(device)
            correct += (model(xb).argmax(dim=1) == yb).sum().item()
    model.train()
    return correct / len(X)


def train_step(model, opt, xb, yb):
    loss = F.cross_entropy(model(xb), yb)
    opt.zero_grad()
    loss.backward()
    opt.step()
    return loss


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=400)
    p.add_argument("--batch", type=int, default=64)
    p.add_argument("--profile", action="store_true", help="profile steps 50-60 and exit")
    args = p.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    name = torch.cuda.get_device_name(0) if device.type == "cuda" else "CPU"
    print("device: %s (%s)" % (device, name))

    rng = np.random.default_rng(0)
    torch.manual_seed(0)
    train_x, train_y = make_images(5000, rng)
    test_x, test_y = make_images(1000, np.random.default_rng(1))

    model = ShapeNet().to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    losses = []

    def one_step():
        # record_function labels each phase, so it shows up by name in the profile
        with record_function("1_augment"):
            idx = rng.integers(0, len(train_x), args.batch)
            xb = augment(train_x[idx], rng)
        with record_function("2_copy_to_device"):
            xb = torch.tensor(xb, dtype=torch.float32).to(device)
            yb = torch.tensor(train_y[idx]).to(device)
        with record_function("3_train_step"):
            loss = train_step(model, opt, xb, yb)
        with record_function("4_log_loss"):
            losses.append(loss.item())

    if args.profile:
        from torch.profiler import ProfilerActivity, profile
        for _ in range(50):          # warm-up: skip one-off setup costs
            one_step()
        acts = [ProfilerActivity.CPU] + ([ProfilerActivity.CUDA] if device.type == "cuda" else [])
        with profile(activities=acts) as prof:
            for _ in range(10):
                one_step()
        for key in ("self_device_time_total", "self_cuda_time_total", "self_cpu_time_total"):
            try:
                print(prof.key_averages().table(sort_by=key, row_limit=15))
                break
            except Exception:
                continue
        print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=15))
        prof.export_chrome_trace("trace.json")
        print("wrote trace.json (open it at https://ui.perfetto.dev)")
        return

    t_start = None
    for step in range(1, args.steps + 1):
        if step == 11:               # skip the first steps when timing
            t_start = time.perf_counter()
        one_step()
        if step % 20 == 0:
            acc = accuracy(model, train_x, train_y, device)
            print("step %4d  loss %.4f  train accuracy %.1f%%" % (step, np.mean(losses[-20:]), 100 * acc))
    if device.type == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - t_start

    print("\ntime per step: %.2f ms" % (1000 * elapsed / (args.steps - 10)))
    print("test accuracy: %.1f%%" % (100 * accuracy(model, test_x, test_y, device)))


if __name__ == "__main__":
    main()
