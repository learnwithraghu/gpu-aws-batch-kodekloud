# Video 05 — The catalog file and the AWS map
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay. Here's the thing that actually ships.

The product of this course is not a running GPU. It is the CSV KodeFood reads.

descriptions.csv has three columns. image_s3_uri, item_description, and photo_status. Each row ties one photo's address in S3 to a short sentence and an accepted or rejected status. For the sample folder, a row can point at images/sample/bowl.jpg, say a food dish of noodles with vegetables, and mark accepted. A car photo can say a car parked on the street and mark rejected. The app uses the accepted rows when someone opens the menu. It does not run BLIP on the request. Captioning is too slow to sit on a page load. The heavy work already happened. The app just reads the result. If the CSV is wrong, the menu is wrong, even when the GPU job looked fine.

Three AWS pieces hold that, and they hold different things.

S3 is the data. The photos go in, and the CSV stays after the GPU is gone.

ECR is the program. It is a private registry for the image that already has CUDA, PyTorch, and the caption code, so a fresh machine does not need you to install any of that by hand.

Batch is the scheduler. It starts a GPU only long enough to pull that image, read the photos, write the captions, and mark each one accepted or rejected. Then the machine can disappear. The file cannot.

So the path is short. Photos land in S3 under images and the folder name. You build the image and push it to ECR. A Batch job pulls it, reads the photos, and writes descriptions, the folder name, and descriptions.csv. KodeFood only knows about that file. It does not need to know which machine ran, or whether that machine is still up.

Next we look at what Batch actually is. A scheduler for a container that starts, runs, and exits. Not a notebook you leave open over SSH.
