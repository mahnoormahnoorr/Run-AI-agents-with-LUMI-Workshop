# Warm-up: know your setup

About 15 minutes · no compute · nothing to submit

Before you hand any real work to an agent, find out what you are working with: which LLM is answering, where it runs, what it can see, and whether its answers about LUMI hold up.
Start OpenCode in an empty folder and work through these with the agent. Ask for links to the LUMI documentation wherever the answer is about LUMI, and open at least two of them.

The questions:

1. What LLM are you, and where does it physically run? Compare the agent's answer with the status line in OpenCode. Which one do you trust?
2. Which tools can you use? Which of them can you use without asking me, and which need my permission first? Ask it, then test one of each.
3. List the files in my home directory and in my project's /scratch folder, and explain the result. 
4. What does a LUMI-G node contain? Tell me the GPUs, how many GPU devices Slurm sees, the number of CPU cores and the memory. Use the LUMI documentation and include links.
5. Which storage areas does my LUMI project have, what is each one for, and is any of it backed up? Use the LUMI documentation and include links.
6. Is LUMI healthy right now? Are there any incidents or planned maintenance? Compare the agent's answer with status.lumi.csc.fi.
7. Which command should I run myself to see how much compute my project has left? You can't run it from inside the container. The agent cannot check this from inside the container. Ask it which command you should run, run it yourself in your second terminal, then paste the output back and ask the agent to explain it.
8. Trick question: "How do I install CUDA 12 on LUMI?" What should a good answer say?


The exercise is done when when you can say which LLM you used and where it runs, describe a LUMI-G node, explain where your files belong (and that you need your own backups), and say how much compute your project has left — each backed by a documentation link or by output you ran yourself.

If anything failed or gave an answer you didn't expect, flag it to the organisers. 

