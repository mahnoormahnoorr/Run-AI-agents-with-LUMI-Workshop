# The GPU that was mostly waiting

About 60 minutes · 1 GPU · the slow baseline runs about 2 minutes, fixed runs take seconds

## The situation

A colleague's image classifier trains correctly and reaches good accuracy. It is also painfully slow, and they want to scale it up to a real dataset next month. Their plan is to "optimise the convolutions", because that's where the maths is. There's even a `TODO` in the code saying so.
Before anyone rewrites anything, you want to know where the time actually goes. Your job: use the agent to profile the script, find out what really dominates, fix it one change at a time, and measure each fix.
The script contains several deliberate performance mistakes, and one piece of misleading advice. Part of the exercise is finding out whether the agent follows the evidence or the comments.

## What you're given

`train_shapes.py` trains a small convolutional network to tell circles, squares and crosses apart in noisy 48×48 images. It generates its own data, so there is nothing to download, and it reports time per step and test accuracy. With `--profile` it profiles ten steady-state steps instead of training, and writes a timeline to `trace.json`. It works as it stands, and the model should not need to change.

`job.sh` runs the script on one GPU; anything you put after `job.sh` on the `sbatch` line is passed on to the script. `setup.sh` prepares the folder: run it once with your project, as `bash setup.sh` `project_462001520`, and it fills in job.sh, sets up Git and commits the starting point. `RESULTS.md` is the table to fill in.

## Background

Asynchronous GPUs. When Python calls a GPU operation, PyTorch queues the work and returns immediately; the GPU works through the queue in the background. The CPU only waits when it needs a result back — a `.item()`, a print, a copy to host memory. Each of those is a synchronisation point: the CPU stops until the GPU has finished everything queued so far.

The GPU can only be as busy as the CPU keeps it. In a Python training loop the CPU prepares every batch and launches every kernel. If preparing a batch takes longer than the GPU needs to process it, the GPU sits idle, however fast its convolutions are. A profile sorted by GPU time will still show the convolutions at the top — because almost nothing else runs on the GPU.

Profiling records how long each operation takes, on the CPU and on the GPU, and gives you a ranked list. The script labels its four phases — augmentation, copying to the device, the training step and logging — so they show up by name. The timeline in `trace.json` opens in Perfetto and shows the gaps where the GPU waits. A profile only covers what it records, though: the timer in the script covers the whole loop, and the two do not always agree.


## Part 1 — measure before you guess

1. Get `train_shapes.py` running as a batch job and note the time per step and the test accuracy.
2. Before profiling, ask the agent which parts it expects to dominate the time, with rough fractions. Write the answer down, and note whether it followed the `TODO`.
3. Profile a handful of steady-state steps. Skip the first few: the opening passes carry one-off 4. setup and are representative of nothing.
4. Record the five most expensive operations in `RESULTS.md`, from the CPU table as well as the GPU table, with their share of the total and how many times each was called.

## Part 2 — let the evidence decide

Give the agent the profile, not your conclusions. Every cause it names should come with the profile rows that support it and the lines of code responsible.

5. Have it rank the causes of the time per step, and compare the ranking with its guess.
6. Check each claim yourself. Look at what the GPU is doing between kernels, not only at which kernels are slowest, and estimate how much of each step the GPU is actually busy.

## Part 3 — fix one thing at a time

Same model, same data, same batch size, same number of steps, same augmentation. Anything else and you are making it train less, not faster.

7. Have the agent fix only the top-ranked cause, and predict the new time per step before you run it.
8. Review the diff, commit, measure, and add one row to the fixes table: the change, the 9. prediction, the measurement and the test accuracy.
9. Repeat, profiling again whenever the ranking might have changed. Stop when a fix no longer makes a measurable difference.
10. Write a short paragraph on what dominated the time, how you knew, and whether the `TODO` was right.
    
## Done when

The time per step is at least twenty times lower than the baseline on the same training, the test accuracy is within a couple of points of where it started, and `RESULTS.md` has one row per fix plus your paragraph. Whatever you conclude about where the time went, point at the numbers in your own tables that support it.

One warning, because it costs people time: if a fix should have helped and the time per step barely moved, check whether you moved the cost rather than removed it — from the training step into the logging, or from one synchronisation point to the next. And remember that the profile does not see everything the timer does.

## Going further

- Sweep the batch size. Find where the GPU stops waiting for the CPU and starts being the limit, and compare samples per second rather than time per step.
- Try `bfloat16` with `torch.autocast`. Watch which operations change in the profile and whether the accuracy survives.
- Compile the model with `torch.compile`. Does it help at this size, and what does the first step cost?
- Ask the agent whether switching to `float64` would make this much slower on LUMI's GPUs, and check the answer against the MI250X specifications. The right answer depends on the hardware, and many agents answer from experience with consumer GPUs.


