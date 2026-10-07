#!/usr/bin/env python3
"""Estimate pi by random sampling for one config. Standard library only."""
import json
import os
import random
import socket
import sys
import time


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: process.py configs/config_XX.json")
    with open(sys.argv[1]) as f:
        cfg = json.load(f)
    if cfg["n"] <= 0:
        sys.exit("config %s: n must be positive" % cfg["id"])

    rng = random.Random(cfg["seed"])
    t0 = time.time()
    inside = 0
    for _ in range(cfg["n"]):
        x, y = rng.random(), rng.random()
        if x * x + y * y <= 1.0:
            inside += 1
    estimate = 4.0 * inside / cfg["n"]

    os.makedirs("results", exist_ok=True)
    out = {
        "id": cfg["id"],
        "n": cfg["n"],
        "pi_estimate": estimate,
        "seconds": round(time.time() - t0, 3),
        "host": socket.gethostname(),
        "array_task": os.environ.get("SLURM_ARRAY_TASK_ID"),
    }
    with open(os.path.join("results", "result_%02d.json" % cfg["id"]), "w") as f:
        json.dump(out, f)
    print("config %02d: pi ~ %.5f (%s s on %s)" % (cfg["id"], estimate, out["seconds"], out["host"]))


if __name__ == "__main__":
    main()
