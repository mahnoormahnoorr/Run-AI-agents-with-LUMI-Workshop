# Setup (works on my laptop)

```bash
conda create -n trainenv python=3.11 -y
conda activate trainenv
pip install -r requirements.txt

nvidia-smi                      # check the GPU is there
export CUDA_VISIBLE_DEVICES=0
python train_small.py
```

Takes about a minute on my RTX laptop GPU.
