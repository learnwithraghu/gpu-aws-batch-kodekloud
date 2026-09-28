# Lesson 00 — The catalog

A vendor uploads one folder of dish photos. One GPU run later, the food app has one catalog file: a short description for every photo.

No AWS commands in this lesson.

## Vendor upload

Photos land in the images bucket under one folder:

```
s3://<images-bucket>/images/<batch>/
```

A typical vendor batch is about 25–30 photos. The folder name (`<batch>`) is what later lessons call the batch stem. `sample` is the stem used in the commands below.

## One run, one file

One job reads every `.jpg`, `.jpeg`, and `.png` in that folder. It writes a single CSV when it has a description for each photo. Photos in other folders are a different run.

Groups of 8 inside the job are only how many photos the GPU holds at once. They do not create extra files.

## Catalog CSV

```
s3://<descriptions-bucket>/descriptions/<batch>/descriptions.csv
```

```csv
image_s3_uri,item_description
s3://<images-bucket>/images/sample/bowl.jpg,a food dish of noodles with vegetables
```

The column is named `item_description`. That text is the catalog line for the dish.

## What the food app reads

Each row is one dish: where the photo lives, and the catalog sentence for it. The app does not read the image folder. It reads this CSV.
