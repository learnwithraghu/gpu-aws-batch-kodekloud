# Video 03 — Batch vs always-on GPU
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. Let's talk about the bill.

You could leave a g4dn.xlarge running all day for KodeFood. It would caption a vendor folder whenever one showed up. It would also cost money when the queue is empty.

Vendors upload all the time across two thousand shops, but that does not mean you want one GPU reserved for each of them. The right shape is a shared pool. When folders are waiting, Batch starts machines. When the queue is empty, capacity can go back to zero. You pay for the minutes the jobs need. Idle time with nothing queued is not on the bill.

That pool setting is minimum vCPUs set to zero on the compute environment. A folder lands, Batch starts an instance, the captions run, the CSV shows up with accepted and rejected rows, and the instance can go away.

Always-on is still the right bill for a different product. Fraud scoring on every click needs an answer in milliseconds, so the GPU has to already be warm. KodeFood's photo check has a defined end. That end is when the CSV lands. After that, nothing is waiting on that machine, and it can leave.

Next is the contract that makes that moment obvious. One vendor folder comes in. One file goes out.
