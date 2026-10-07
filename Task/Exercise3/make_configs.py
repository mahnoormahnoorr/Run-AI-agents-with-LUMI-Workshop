#!/usr/bin/env python3
"""Create 20 small config files in configs/."""
import json
import os

os.makedirs("configs", exist_ok=True)
for i in range(20):
    cfg = {"id": i, "n": 200000 + 50000 * i, "seed": 1000 + i}
    with open(os.path.join("configs", "config_%02d.json" % i), "w") as f:
        json.dump(cfg, f)
print("wrote 20 configs to configs/")
