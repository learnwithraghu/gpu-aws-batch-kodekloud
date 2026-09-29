# Video 05 — The catalog file and the AWS map
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

The product is the CSV. descriptions.csv has two columns, image_s3_uri and item_description. Each row ties one photo's address in S3 to a short sentence. For the sample folder, one row can point at images/sample/bowl.jpg and say a food dish of noodles with vegetables. The food app reads this file. It does not open the image folder to invent titles. For this offline pipeline it does not re-run BLIP when someone loads the menu. If the CSV is wrong, the app is wrong, even when the GPU ran fine. Later lessons judge success by that object existing, and by one row per photo.

Captioning is expensive and slow next to an ordinary HTTP request. Precomputing the catalog text keeps the app load fast. It also separates a model release from a mobile deploy. You can ship a new CSV without shipping a new app. YouTube does the same thing with pre-rendered thumbnails. The heavy work happens ahead of the viewer. The app just reads the result.

Three AWS pieces show up after this lesson, and each one holds something different. S3 is object storage. It is there so the photos and the CSV survive after the GPU is gone. Durable input and output, across machines that do not stay up. Lessons five, six, and nine use it. ECR is the private Docker registry. The instance pulls a pinned image that contains CUDA, PyTorch, and your code. Lessons three and four build that image and push it. AWS Batch is the job scheduler. It starts a GPU machine to run that image, and it does that without leaving a GPU on overnight. Lessons one, seven, and eight are the scheduler.

Say what each of the three pieces holds. S3 is data. It holds the photos going in and the catalog CSV coming out. ECR is the program and its dependencies. The image carries CUDA, PyTorch, and your code, so a fresh machine can run the caption model without you installing anything by hand. Batch is the scheduler. It turns those two, the data and the program, into a finished CSV, and it does that without leaving a GPU on overnight.

Say the flow in one pass. Photos sync to S3, under images, then the folder name. You build the image and push it to ECR. A Batch job pulls that image, reads the photos from S3, and writes descriptions, then the folder name, then descriptions.csv. The app reads only that CSV. It never has to know which GPU ran, or whether the machine is still up. The machine is allowed to be gone. The file has to be there, with image_s3_uri and item_description, one row per photo.

On the screen, three pillars stand in a row, S3, ECR, and Batch, with arrows between them. The app's arrow touches only the CSV in S3.

Next is what AWS Batch actually is. A scheduler for a container that starts, runs to the end, and exits. A notebook you SSH into is a different tool.
