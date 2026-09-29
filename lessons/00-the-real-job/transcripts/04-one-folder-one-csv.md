# Video 04 — One folder, one CSV
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** A **batch contract**: one **input location** (S3 prefix with photos), one **output object** (catalog CSV for that batch). Internal micro-batches do **not** multiply output files.

**Why contracts matter.** Downstream apps (mobile menu, CMS) integrate against **stable paths**, not “whatever file the GPU felt like writing.” Operations can alert on **missing object** instead of parsing ambiguous logs.

**Example keys.** Input: **`images/<batch>/`** in the images bucket — `<batch>` might be **`sample`**. Output: **`descriptions/<batch>/descriptions.csv`** in the CSV bucket. Eight photos processed together still append rows to **one** file.

**Success criterion for the course.** Not merely “container exited 0” but **object exists**, **schema correct**, **one row per supported photo**.

**Visual:** One folder icon → one CSV icon; micro-batch loops drawn **inside** the GPU box, single arrow to CSV.

CSV as the product the app reads — next.
