# Video 004 — Inside the GPU: Hardware Explained

**Section:** 002 — GPU Fundamentals: From Silicon to Cloud
**Lecture#:** 004
**Sheet title:** Inside the GPU: Hardware Explained
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 002-004-inside-the-gpu--hardware-expla

---

When engineers choose a GPU for a workload, they do not just ask "how fast is the chip?" They look inside the hardware at three things: compute cores, memory capacity, and the bus that connects the GPU to the rest of the machine.

Let’s start with the compute side. Inside an NVIDIA data-center GPU—like the T4 we use for KodeFood—work is organized into Streaming Multiprocessors. Each one contains standard CUDA cores for general parallel math, plus specialized Tensor Cores built specifically to accelerate the matrix multiplications inside deep learning models.

Now here is the catch. Those thousands of cores are only fast if data is already sitting right next to them.

That brings us to the most important operational limit on any GPU: VRAM, or video memory. VRAM is high-bandwidth memory soldered directly onto the GPU board. It is completely separate from the EC2 instance’s system RAM.

Before our job can caption a single dish photo, the vision model’s weights have to be loaded into VRAM. Then, every image we process in a micro-batch adds activation tensors on top of those weights.

What happens if we try to push thirty high-resolution photos through the GPU in one giant step? Even if the host machine has plenty of spare system RAM, the GPU’s own 16 gigabytes of VRAM can fill up and crash the process with a CUDA out-of-memory error. Adding host RAM will never fix a VRAM limit.

Finally, there is the PCIe link between host RAM and GPU VRAM. Copying data across that bridge takes time. Once the model weights are loaded onto the GPU, we want to keep them there and stream small micro-batches of images through until the vendor folder is finished.

Keep those three pieces in mind: cores determine how fast the math runs, VRAM determines how large a model and micro-batch fit at once, and the host-to-GPU link explains why we load the model once per job.

Next, let’s take this hardware out of the server room and see how cloud providers expose GPUs as rent-by-the-minute infrastructure.

---

## Further reading (not spoken)

- [NVIDIA Tesla T4 Tensor Core GPU Datasheet](https://www.nvidia.com/en-us/data-center/tesla-t4/) — architecture of the T4 accelerator (Streaming Multiprocessors, Tensor Cores, 16 GB GDDR6 VRAM)
- [PyTorch Documentation: CUDA Semantics and Memory Management](https://pytorch.org/docs/stable/notes/cuda.html) — how device memory (VRAM) behaves separately from host RAM
