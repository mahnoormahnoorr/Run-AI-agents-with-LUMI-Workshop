# Facilitator notes — The GPU that was mostly waiting

**Keep this file away from participants**, e.g. on a separate branch.

## Before the workshop

- [ ] Put the real container path in `SIF_PATH` at the top of `materials/setup.sh`.
- [ ] Run the exercise once on LUMI: `bash setup.sh <project>`, `sbatch job.sh`, `sbatch job.sh --profile`.
- [ ] Check the profile shows the labelled phases (`1_augment`, `2_copy_to_device`, `3_train_step`, `4_log_loss`) with the workshop's PyTorch version, and that the baseline takes roughly 2 minutes.
- [ ] Note the baseline time per step and test accuracy, to compare with participants' numbers.


**The planted problems**, in the order they should surface (measured costs depend on the node; the shape of the sequence is what matters):

| # | Problem | Where | Why it's slow | How it shows up |
| --- | --- | --- | --- | --- |
| 1 | **Per-pixel Python augmentation** | `augment()` | Two nested Python loops and one `rng.normal` call per pixel: ~147 000 Python-level calls per batch of 64, on one CPU core. ~160 ms per step on a typical CPU | `1_augment` dominates the CPU table; on the GPU timeline, long idle gaps between short bursts |
| 2 | **Full-training-set evaluation every 20 steps, in batches of 16** | `accuracy()` and the logging block | 313 tiny batches, each copied from the CPU and synchronised with `.item()`. Inside the timed loop, so it counts towards time per step | **Not in the profile at all**: `--profile` only profiles `one_step()`. Only the overall timer reveals it, typically after fix 1 |
| 3 | **float64 NumPy → new tensor → copy, every step** | `2_copy_to_device` | Allocates and converts on the CPU, then a blocking host-to-device copy | Visible in `2_copy_to_device` once fix 1 is done |
| 4 | **`loss.item()` every step** | `4_log_loss` | Forces the CPU to wait for the GPU every step, so the CPU can't queue the next step's work ahead | `4_log_loss` takes as long as the GPU work it waits for |
| 5 | **A new constant tensor in every forward pass** | `ShapeNet.forward` | `torch.tensor([0.25]).to(x.device)` allocates and copies a tensor every call | Small `aten::to`/`aten::copy_` entries inside `3_train_step` |
| — | **Red herring: "optimise the convolutions"** | `TODO` comment | The convolutions take a tiny fraction of the step at this size | Convolution kernels are near the top of the *GPU* table only because almost nothing else runs on the GPU; the GPU is idle most of the time |

**Expected result:** from ~170 ms per step to a few milliseconds, a 30–80× speedup, with test accuracy unchanged within noise. Participants should reach at least 20× with fixes 1 and 2 alone.

**The lessons to draw out in discussion:**

- **The GPU table lies by omission.** Sorting by GPU time shows convolutions on top, which seems to confirm the `TODO`. The CPU table and the timeline show the GPU is mostly idle. Agents that only read the top of the GPU table fall for this.
- **The profile isn't the whole program.** Fix 2 is invisible in `--profile`. Participants who only trust the profile get stuck after fix 1, which is what the warning in the exercise is about.
- **Fixes move costs around.** After fix 1, `.item()` (fix 4) may look like the new top cost, because it now waits for GPU work that used to overlap with augmentation.

**Reference changes** (untested with PyTorch here; syntax-checked):

```python
# --- model: keep the constant on the device, created once ---
class ShapeNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.fc1 = nn.Linear(32 * 12 * 12, 64)
        self.fc2 = nn.Linear(64, 3)
        self.register_buffer("mean", torch.tensor([0.25]))

    def forward(self, x):
        x = (x - self.mean) / 0.5
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        return self.fc2(F.relu(self.fc1(x.flatten(1))))


# --- augmentation: same behaviour, whole batch at once, on the GPU ---
def augment_gpu(xb):
    n = xb.shape[0]
    flip_h = (torch.rand(n, device=xb.device) < 0.5)[:, None, None, None]
    flip_v = (torch.rand(n, device=xb.device) < 0.5)[:, None, None, None]
    xb = torch.where(flip_h, xb.flip(3), xb)
    xb = torch.where(flip_v, xb.flip(2), xb)
    return xb + 0.1 * torch.randn_like(xb)


# --- evaluation: whole set in a few large batches, data already on the GPU ---
def accuracy(model, X, y, batch=1000):
    model.eval()
    with torch.no_grad():
        correct = sum((model(X[i:i + batch]).argmax(1) == y[i:i + batch]).sum()
                      for i in range(0, len(X), batch))
    model.train()
    return correct.item() / len(X)


# --- in main(): move the data to the GPU once, as float32 ---
train_x_t = torch.tensor(train_x, dtype=torch.float32, device=device)
train_y_t = torch.tensor(train_y, device=device)
test_x_t = torch.tensor(test_x, dtype=torch.float32, device=device)
test_y_t = torch.tensor(test_y, device=device)

def one_step():
    idx = torch.randint(0, len(train_x_t), (args.batch,), device=device)
    loss = train_step(model, opt, augment_gpu(train_x_t[idx]), train_y_t[idx])
    losses.append(loss.detach())             # no synchronisation here

# --- logging: synchronise once every 20 steps, not every step ---
if step % 20 == 0:
    mean_loss = torch.stack(losses[-20:]).mean().item()
    acc = accuracy(model, train_x_t, train_y_t)
```

Moving the random number generation from NumPy to PyTorch changes the exact random sequence, so test accuracy will differ by a fraction of a point between runs: that's noise, not a regression.

**Things agents often get wrong here:**

- **Following the `TODO`**: proposing cuDNN/MIOpen tuning, channels-last layouts or a custom kernel for a convolution that takes a tiny share of the step.
- **Vectorising augmentation in NumPy** but leaving it on the CPU. A big improvement, but the copy and synchronisation remain; it's a valid intermediate step, not the end.
- **Changing the behaviour**: dropping the noise, flipping the whole batch the same way, or reducing the steps or batch size to "speed it up". The diff review in step 7 should catch this.
- **Removing the evaluation** instead of making it cheap, then claiming the speedup.
- **Calling `torch.cuda.synchronize()` everywhere** "to get accurate timings", which reintroduces the problem it's measuring.

**The float64 trick question:** the MI250X has strong FP64 support, so FP64 is much less of a penalty than on consumer GPUs. The right answer cites the per-GCD FP64 vs FP32 figures from the LUMI or AMD documentation *(verify the numbers)*. Memory use and bandwidth still double, which is the real cost here.
