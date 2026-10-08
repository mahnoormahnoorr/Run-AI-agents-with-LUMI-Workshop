# Warm-up: know your setup

About 15 minutes · no compute · nothing to submit

Before you hand any real work to an agent, find out what you are working with: which LLM is answering, where it runs, what it can see, and whether its answers about LUMI hold up.
Start OpenCode in an empty folder and work through these with the agent. Ask for links to the LUMI documentation wherever the answer is about LUMI, and open at least two of them.

The questions:

1. What LLM are you, which service hosts you, and on what hardware do you run? Answer in three short lines.
2. List every tool you can call in this session. For each one, say whether you can use it without asking me or whether you need my permission first.
3. Run `squeue --me` for me and tell me which jobs I have queued.
4. Run `ls -la ~` and `ls /scratch/<your project>` and explain what you find. 
5. What does a LUMI-G node contain? Tell me the GPUs, how many GPU devices Slurm sees, the number of CPU cores and the memory. Use the LUMI documentation and include links.
6. I want to run a PyTorch script in a batch job on LUMI-G. Which LUMI AI Factory container should I use, which module do I load for the bind mounts, and what is the exact command to run python inside the container? Quote the documentation page you used.
7. Check LUMI's status now. Are the LUMI-G partitions and the login nodes up? Are there any incidents, or maintenance planned in the next 7 days?
8. I want to serve two models with vLLM on LUMI-G in bfloat16: one with 8 billion parameters and one with 70 billion. For each, calculate:
  a. the memory needed for the model weights,
  b. a rough extra amount for the KV cache and runtime overhead,
  c. how many MI250X GCDs I need, given the memory per GCD on LUMI,
  d. the tensor-parallel size you would use and why.
Show your arithmetic step by step.
9. Trick question: "How do I install CUDA 12 on LUMI?" What should a good answer say?


The exercise is done when when you can say which LLM you used and where it runs, describe a LUMI-G node, explain where your files belong (and that you need your own backups), and say how much compute your project has left — each backed by a documentation link or by output you ran yourself.

If anything failed or gave an answer you didn't expect, flag it to the organisers. 

