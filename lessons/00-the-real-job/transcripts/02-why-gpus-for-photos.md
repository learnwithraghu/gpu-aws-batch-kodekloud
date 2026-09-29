# Video 02 — Why GPUs for captioning
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

An image is a large grid of numbers. A caption model turns that grid into text. Inside the model, the work is layers of matrix operations, convolutions and attention, and the result is text tokens. A CPU is strong at sequential work and at logic that branches. It can do this math one operation at a time, or a few at a time. A GPU runs many of those similar operations together.

Both can finish a folder of about twenty-five to thirty photos. The CPU finishes eventually. The GPU finishes the folder in one short run. That is the wait a vendor feels when a catalog is due. It is also why renting a GPU for minutes can beat holding a CPU for hours. This course asks AWS Batch for a GPU instance, a T4, instead of a small CPU box. The claim stops there. It is this model, this batch size, and this latency target. It is not a claim that every AI job needs a GPU.

Walk one photo before the folder. The whole photo is a large grid of numbers, and the model treats that grid as a tensor. Captioning is many matrix steps on that tensor, convolutions and attention, until text tokens come out the other side. A CPU walks those steps mostly in a line. A GPU applies the same step to many numbers at once. Nothing about that requires a new model. It is the finished caption model, run hard, for a short time.

Think of one chef plating every dish alone, and a line kitchen where many hands do the same step on different plates at once. The single chef is the CPU. The line is the GPU. Netflix encodes video frames on parallel hardware for the same reason. The frames are uniform math, and the point is throughput, not a clever branch on each frame. Your folder is that idea at catalog size. About eight photos move together so they fit in GPU memory. The GPU finishes the folder in one short batch job, which is what you want when a vendor is waiting on a catalog and you would rather rent the GPU for minutes than hold a CPU for hours. A small CPU box could still be asked to do this. This course asks AWS Batch for the GPU because the folder should be done in that one short run.

On the screen, a grid of pixel numbers becomes a tensor, then spreads across many GPU cores, and comes out the other side as a text caption. That path is one photo. The folder this course buys the GPU for is about twenty-five to thirty of those photos, done in one short run.

A GPU that stays powered all day is a different bill from a GPU that exists only while a folder is waiting. That cost, always-on versus scale to zero, is next.
