# Video 04 — One folder, one CSV
**Type:** Theory
**Runtime target:** ~3 minutes

---

So, one more piece of the design before we map AWS.

A batch job is easier to trust when it has one input and one output. KodeFood can then look in one place for a vendor's photo check, instead of hunting through a log.

The input is a folder of photos in the images bucket. The path is images, then the folder name. In the commands for this course that name is sample, so the photos live under images/sample/. We only describe jpg, jpeg, and png.

The output is one file in the other bucket. descriptions, then the same folder name, then descriptions.csv. For sample, that is descriptions/sample/descriptions.csv. One job writes that one file. If you point the job at a different vendor folder, the CSV path moves with it.

Inside the GPU the model still sees about eight photos at a time. Those groups are not eight CSVs. Every caption is another row in the same file. Each row has three columns. image_s3_uri, item_description, and photo_status. photo_status is accepted when the caption looks like food, and rejected when it does not. Rejected rows stay in the file so the reason is visible. The app uses the accepted rows for the menu.

A successful file has one row per supported photo. If the container exits cleanly but that file is missing, or a photo has no row, KodeFood still has nothing to show.

Next is who that file is for, and which three AWS pieces hold the photos, the program, and the run.
