# Video 03 — Batch vs always-on GPU
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

An always-on GPU is an EC2 machine, a g4dn.xlarge or something in that family, left running all day whether a vendor uploaded anything or not. A batch design starts a GPU only when a folder is waiting, then lets capacity go back to zero. On the compute environment, that setting is minimum vCPUs set to zero. Instances appear when queued jobs need them. They disappear when the queue is empty. You pay for the minutes the job needs. Idle time between drops is not on the bill.

Food catalogs arrive as rare drops. Hours or days apart. A new vendor. A seasonal menu. A photo reshoot. The work is not a photo every minute. Paying for an idle GPU between those bursts is like leaving a film render farm powered overnight for one scene that might arrive on Tuesday. AWS Batch is how this course gets the other shape. When the compute environment's minimum vCPUs is zero, the spend line stays low and spikes only while captions are running. A GPU you reserve all day is a high flat line.

Leave that g4dn.xlarge running twenty-four hours, whether or not a vendor uploaded anything. That is the flat high line, a reserved GPU, and it includes the overnight hours when the queue is empty. The pulse is the other line. Minimum vCPUs is zero, so while nothing is waiting there is no instance to pay for. A folder shows up, Batch starts a machine, the captions run, the CSV lands, and the line drops. Count an idle night on that reserved line. The queue is empty, the g4dn.xlarge is still up, and the hour still costs money. On the pulse, that same night is a zero. No job is waiting, so there is nothing to bill until the next drop. The spike exists only while captions are running. When the CSV has landed, the line is allowed to fall.

Always-on still wins for a different product. Fraud scoring on every click, or a voice assistant, needs an answer in milliseconds, so the GPU has to already be hot. Those products have no moment where the work is finished and the machine may leave. This workload has a defined end. The end is the moment the CSV lands. After that, nothing is waiting, and the machine can go away. AWS Batch is the tool that draws the spike, and it draws that spike when the compute environment's minimum vCPUs is zero.

On the screen, a dollar chart shows two lines. One is a pulse, spikes only during the caption runs, labeled minimum vCPUs equals zero. The other is a flat high line for the GPU left running. The pulse is the bill this course is built around.

The machine only helps if the job has a clear contract. One folder comes in. One CSV goes out. Next is that contract, the input prefix and the single file the app will read.
