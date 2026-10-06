# Warm-up: know your setup

About 15 minutes · no compute · nothing to submit

Before you hand any real work to an agent, find out what you are working with: which LLM is answering, where it runs, what it can see, and whether its answers about LUMI hold up.
Start OpenCode in an empty folder and work through these with the agent. Ask for links to the LUMI documentation wherever the answer is about LUMI, and open at least two of them.

The questions:

1. Which LLM are you talking to, and where does it physically run? Compare the agent's answer with the status line in OpenCode. Which one do you trust?
2. Which tools can the agent use, and which need your permission? Ask it, then test one of each.
3. What can the agent see? Ask it to list your home directory and your project's /scratch folder. Explain the result.
4. What does a LUMI-G node contain? GPUs, how many GPU devices Slurm sees, CPU cores, memory.
5. Where should your files live? Ask which storage areas your project has, what each is for, and whether any of it is backed up.
6. Is LUMI healthy right now? Compare the agent's answer with status.lumi.csc.fi.
7. How much compute does your project have left? The agent cannot check this from inside the container. Ask it which command you should run, run it yourself in your second terminal, then paste the output back and ask the agent to explain it.
8. Trick question: "How do I install CUDA 12 on LUMI?" What should a good answer say?


The exercise is done when when you can say which LLM you used and where it runs, describe a LUMI-G node, explain where your files belong (and that you need your own backups), and say how much compute your project has left — each backed by a documentation link or by output you ran yourself.

If anything failed or gave an answer you didn't expect, flag it to the organisers. 

