#!/usr/bin/env python3
"""Train a small MLP on synthetic data. Needs no dataset and no internet."""
import argparse
import time

import torch
import torch.nn as nn


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=500)
    p.add_argument("--batch", type=int, default=256)
    p.add_argument("--hidden", type=int, default=1024)
    p.add_argument("--cpu", action="store_true", help="force CPU")
    args = p.parse_args()

    use_gpu = torch.cuda.is_available() and not args.cpu
    device = torch.device("cuda" if use_gpu else "cpu")
    name = torch.cuda.get_device_name(0) if use_gpu else "CPU"
    hip = getattr(torch.version, "hip", None)
    print(f"torch {torch.__version__} | hip {hip} | cuda {torch.version.cuda}")
    print(f"device: {device} ({name}) | visible GPUs: {torch.cuda.device_count()}")

    torch.manual_seed(0)
    n_in, n_out = 128, 10
    # A fixed random "teacher" defines the labels, so the task is learnable.
    teacher = torch.randn(n_in, n_out, device=device)
    model = nn.Sequential(
        nn.Linear(n_in, args.hidden), nn.ReLU(),
        nn.Linear(args.hidden, args.hidden), nn.ReLU(),
        nn.Linear(args.hidden, n_out),
    ).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()

    t_start = None
    for step in range(1, args.steps + 1):
        x = torch.randn(args.batch, n_in, device=device)
        y = (x @ teacher).argmax(dim=1)
        loss = loss_fn(model(x), y)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step == 10:  # skip warm-up steps when timing
            if use_gpu:
                torch.cuda.synchronize()
            t_start = time.perf_counter()
        if step % 50 == 0:
            print(f"step {step:5d}  loss {loss.item():.4f}")

    if use_gpu:
        torch.cuda.synchronize()
    if t_start is not None:
        per_step = (time.perf_counter() - t_start) / (args.steps - 10) * 1000
        print(f"time per step: {per_step:.2f} ms")


if __name__ == "__main__":
    main()
