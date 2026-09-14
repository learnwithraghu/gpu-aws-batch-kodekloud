# S3 Vectors Implementation Handoff

## Current Status

The course is being converted from local NumPy vector search to managed Amazon
S3 Vectors semantic search. The target workflow is:

```text
Video in S3
  -> AWS Batch extracts JPEG frames to S3
  -> AWS Batch GPU job creates CLIP frame embeddings
  -> frame embeddings and metadata are stored in S3 Vectors
  -> local CLIP text embedding queries S3 Vectors
  -> matching S3 frame keys and timestamps are displayed
```

### Completed

- Confirmed S3 Vectors is available in `ap-northeast-1` for AWS account
  `666234783044`.
- Confirmed the installed Boto3 version supports `s3vectors`.
- Created the live S3 Vectors resources:
  - Vector bucket: `gpu-teaching-vectors-666234783044`
  - Vector index: `video-frames`
  - Data type: `float32`
  - Dimensions: `512`
  - Distance metric: `cosine`
- Added [`.env.example`](.env.example) with `S3_VECTOR_BUCKET` and
  `S3_VECTOR_INDEX`.
- Added [helpers/s3_vectors.py](helpers/s3_vectors.py), which validates
  512-dimension finite, non-zero embeddings, creates stable frame record keys,
  and batches `PutVectors` requests in groups of up to 500.
- Added [helpers/setup_s3_vectors.py](helpers/setup_s3_vectors.py), an
  idempotent setup helper. It derives the default vector bucket from the AWS
  account ID and creates the bucket/index when absent.
- Updated [Dockerfile](Dockerfile) to require `boto3>=1.43.93` and copy the
  shared vector helper into the Batch container image.
- Updated [lessons/03-video-to-frames/extract_frames.py](lessons/03-video-to-frames/extract_frames.py)
  to write `frames/<video-stem>/manifest.json`. Each entry contains a frame key,
  frame index, source frame index, and timestamp in milliseconds.
- Updated [lessons/04-frames-to-embeddings/embed_frames.py](lessons/04-frames-to-embeddings/embed_frames.py)
  to read the frame manifest and upsert CLIP embeddings to S3 Vectors instead
  of writing `embeddings.npy` and `frame_keys.json`.
- Updated the Lesson 04, Lesson 06, and Lesson 07 Batch submission scripts to
  pass `S3_VECTOR_BUCKET` and `S3_VECTOR_INDEX` into embedding jobs.
- Updated [lessons/05-vector-search/notebook.ipynb](lessons/05-vector-search/notebook.ipynb)
  and [lessons/05-vector-search/README.md](lessons/05-vector-search/README.md)
  to query S3 Vectors rather than downloading and scanning a NumPy matrix.
- Validated the live index with an empty `QueryVectors` request using a valid
  normalized 512-dimension test vector.
- Validated Python syntax for the new helpers and changed worker/submission
  scripts, plus `git diff --check` at the point those changes were made.

## Important Deployment Prerequisites

1. Add these values to the local `.env` file before submitting Lesson 04, 06,
   or 07 Batch jobs:

   ```dotenv
   S3_VECTOR_BUCKET=gpu-teaching-vectors-666234783044
   S3_VECTOR_INDEX=video-frames
   ```

2. Update the AWS Batch job role, `BatchJobRole`, to allow writes to the vector
   index. At minimum, grant `s3vectors:PutVectors` for the course index.

3. Rebuild and push the Docker image after the Dockerfile change. The currently
   pushed image does not yet contain `helpers/s3_vectors.py` or the required
   Boto3 version.

4. The IAM identity used locally needs S3 Vectors access for setup/query and
   cleanup. Required actions include:

   ```text
   s3vectors:CreateVectorBucket
   s3vectors:GetVectorBucket
   s3vectors:CreateIndex
   s3vectors:GetIndex
   s3vectors:ListVectorBuckets
   s3vectors:PutVectors
   s3vectors:QueryVectors
   s3vectors:DeleteIndex
   s3vectors:DeleteVectorBucket
   ```

## Remaining Implementation

1. Complete documentation rewrite for the root README and Lessons 03, 04, 06,
   and 07. Remove stale references to `embeddings.npy`, `frame_keys.json`, and
   local NumPy nearest-neighbour search. Document that normal S3 stores media
   while S3 Vectors stores searchable embeddings plus metadata.

2. Review and update the Lesson 04 notebook. Its current inspection and PCA
   cells still download `embeddings.npy`; replace those cells with index
   inspection and an explanation of vector records. Remove PCA or make it an
   optional, explicitly sampled diagnostic rather than the source of truth.

3. Update the Lesson 06 notebook and README verification step. It should check
   that the frame manifest exists in normal S3 and that S3 Vectors returns
   matches for the relevant video, instead of checking for old embedding files.

4. Update the Lesson 07 notebook and README completion diagram. The final
   storage destination is `S3 Vectors`, not `CLIP embeddings in S3`.

5. Update [helpers/teardown.py](helpers/teardown.py) and
   [helpers/README.md](helpers/README.md) with an explicit
   `--delete-s3-vectors` option. Delete the index before the vector bucket and
   poll until each deletion completes. Do not delete S3 Vectors unless that
   option is supplied.

6. Add focused tests, preferably using Botocore `Stubber`, for:
   - 512-dimension, finite-value, and non-zero-vector validation.
   - Stable vector keys and frame metadata serialization.
   - Splitting `PutVectors` payloads at 500 records.
   - Mapping `QueryVectors` response metadata to normal S3 frame objects.
   - Missing S3 Vectors configuration errors.
   - Index-before-bucket teardown order.

7. Review `lessons/07-scale-and-cost/submit_array_job.py`. It still performs a
   runtime `pip install awscli` inside the Batch container even though that is
   unrelated to selecting an array input. Remove it or replace it with a small
   committed worker script in a later cleanup.

## Required Validation Sequence

1. Rebuild and push the shared Batch image:

   ```bash
   docker build -t gpu-teaching .
   # Tag and push using the existing root README instructions.
   ```

2. Register a new Batch job-definition revision that points to the newly pushed
   image and includes the Batch job role permission for `s3vectors:PutVectors`.

3. Run Lesson 03 for a small sample video. Confirm both frames and
   `frames/sample/manifest.json` exist in the ordinary S3 bucket.

4. Run Lesson 04. Confirm it succeeds and that S3 Vectors contains exactly one
   record per extracted frame. Use `QueryVectors` with a normalized 512-dimension
   query vector and verify returned metadata includes `frame_key`, `frame_index`,
   `timestamp_ms`, and `video_stem`.

5. Run the Lesson 05 notebook. Check that a text query returns results and each
   returned `frame_key` loads an existing JPEG from the ordinary S3 bucket.

6. Run Lesson 06 with the sample video, then a small Lesson 07 array job. Verify
   different videos use distinct vector keys such as
   `<video-stem>/frame_00000`, avoiding cross-video overwrites.

7. Run the expanded teardown in a disposable environment with
   `--delete-s3-vectors`; verify the index is deleted before the vector bucket.

## Operational Notes

- S3 Vector buckets and indexes are regional. Keep Batch, normal S3, and S3
  Vectors in `ap-northeast-1` for this course.
- The vectors are CLIP `ViT-B/32` image embeddings and must remain 512
  dimensions. Text queries must use the same CLIP model and normalization.
- Use cosine distance because both image and text embeddings are normalized to
  unit length.
- Existing `embeddings.npy` artifacts are intentionally not migrated. Rerun
  Lesson 04 to populate S3 Vectors.
- The vector bucket and index above are live AWS resources. They are currently
  empty but may incur service charges according to AWS S3 Vectors pricing.