# Lesson 07 — Read the catalog

Print the CSV the food app would read. The job in lesson 06 must already be `SUCCEEDED`.

## The command

```bash
python lessons/07-read-the-catalog/show_descriptions.py --batch-stem sample
```

`--batch-stem` must match the stem you submitted. `sample` reads `descriptions/sample/descriptions.csv` from `S3_CSV_BUCKET`.

## How to read a row

The script prints the description, then the image URI:

```
  1. a food dish of dumplings on a plate
      s3://<images-bucket>/images/sample/plate.jpg
```

The number of lines in the header (`7 descriptions in s3://...`) is the number of photos the job described, not the number of files.

## The file in S3

The same object is the catalog:

```
s3://<csv-bucket>/descriptions/sample/descriptions.csv
```

It has a header and one data row per photo:

```csv
image_s3_uri,item_description
```

Download it with `aws s3 cp` if you want the file itself. `show_descriptions.py` only prints it.
