# Step 02 — Create the ECR repository

Amazon ECR is AWS's private Docker registry. Batch pulls from it natively
using IAM — no registry credentials to manage.

**Run (once):**

```bash
aws ecr create-repository \
  --repository-name gpu-teaching \
  --region ap-northeast-1
```

**Expected:** JSON output containing the repository URI — or
`RepositoryAlreadyExistsException`, which is fine, just continue.
