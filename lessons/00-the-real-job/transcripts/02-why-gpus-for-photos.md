# Video 02 — Why GPUs for captioning
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay, so why a GPU for this?

A photo is a big grid of numbers. A caption model turns that grid into a sentence, and almost all of the work inside is the same kind of math. Matrix multiplies, convolutions, attention, until text comes out the other side.

A CPU is good at work that changes direction. If this, then that. It can do the matrix math too, but mostly a little at a time. A GPU is built to run the same operation across a huge pile of numbers at once. Think of one cook plating every dish alone, versus a line where several people do the same step on different plates. The cook is the CPU. The line is the GPU.

Both will finish one KodeFood vendor folder of twenty-five or thirty photos. The CPU finishes later. The GPU finishes the folder in one short run. That is the wait the ops team feels when vendors are uploading, and it is why this course asks Batch for a GPU machine, a T4, instead of a small CPU box. I am not saying every AI job needs a GPU. I am saying this model, on this many photos, should be done in minutes.

About eight photos go through together. That number is memory. It is how many of those grids fit on the card at once. The folder is still one job, and each caption still becomes an accept or a reject.

Next is the bill. KodeFood does not keep a GPU switched on per vendor. A shared pool that only exists while folders are waiting is a different cost from a machine left on all day.
