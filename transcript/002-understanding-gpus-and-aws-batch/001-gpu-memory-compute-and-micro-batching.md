# Video 001 — GPU Memory, Compute and Micro-Batching
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 001
**Sheet title:** GPU Memory, Compute and Micro-Batching
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-001-gpu-memory--compute-and-micro-

---

We separated CPU orchestration from GPU math. The next limit students hit is not “is there a GPU?” but “how much can it hold at once?”

GPU memory — often called VRAM — is finite and separate from the instance’s system RAM. Loading BLIP onto a T4 already consumes a chunk. Each photo you pass through the model adds activations for that forward pass. If you hand the GPU all thirty vendor photos in one call, you can exhaust memory or thrash. The job fails or crawls for a reason that looks mysterious until you think in working sets.

Our application’s answer is micro-batching. The default `BATCH_SIZE` is eight. Thirty photos become groups of eight, eight, eight, and six. Each group is one GPU pass. Captions append to one list. At the end, still one CSV. Micro-batches are a memory tactic, not eight separate product artifacts.

Compute and memory travel together. A bigger batch can raise GPU utilization — more work per kernel launch — but only until VRAM says stop. For KodeFood on a `g4dn.xlarge`, eight is a practical fit for this caption model. You can tune the environment variable later; you should not pretend memory is infinite.

Also keep system RAM in mind. The instance still downloads images and builds the CSV on the CPU side. GPU memory is for the model and the active micro-batch. Confusing those two pools is how teams oversize the wrong resource.

You might wonder where this job should run once we accept that we need a GPU with enough memory for short bursts. Lambda? A long-lived ECS service? SageMaker? Raw EC2? Batch? Next we survey those cloud options with this workload in mind.

---

## Further reading (not spoken)

- https://pytorch.org/docs/stable/notes/cuda.html#memory-management — PyTorch notes on CUDA memory behavior
- https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#features-and-technical-specifications — how GPU device memory constrains concurrent work
