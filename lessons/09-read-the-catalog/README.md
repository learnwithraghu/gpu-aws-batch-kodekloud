# Lesson 09 — Read the catalog

The job in lesson 08 has to be `SUCCEEDED`. This lesson reads the CSV KodeFood would read.

Theory reading: [`theory.md`](theory.md).

```bash
set -a && source .env && set +a
```

## Print it

```bash
aws s3 cp "s3://${S3_CSV_BUCKET}/descriptions/sample/descriptions.csv" -
```

Change `sample` if you submitted a different folder. The file is one header plus one row per photo:

```csv
image_s3_uri,item_description,photo_status
s3://<images-bucket>/images/sample/bowl.jpg,a food dish of noodles with vegetables,accepted
s3://<images-bucket>/images/sample/car.jpg,a car parked on the street,rejected
```

Rejected rows stay in the file. The app uses the accepted rows for the menu.

## Count the rows

```bash
aws s3 cp "s3://${S3_CSV_BUCKET}/descriptions/sample/descriptions.csv" - | wc -l
```

Subtract one for the header. That number is the number of photos the GPU described, not the number of files. There is still one CSV.

To keep a local copy:

```bash
aws s3 cp "s3://${S3_CSV_BUCKET}/descriptions/sample/descriptions.csv" ./descriptions.csv
```
