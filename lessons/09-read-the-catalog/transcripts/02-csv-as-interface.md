# Video 02 — CSV as interface
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What the schema is.** **`image_s3_uri`**, **`item_description`** — column names are **API contract**.

**Why renames break apps.** CMS maps columns to fields; change without migration → production break — like renaming JSON field in public REST API.

**Example row.** `s3://…/images/sample/bowl.jpg`, `A ceramic bowl of ramen with …`

**Visual:** CSV as tiny schema document between ML and product.

Row count check — next.
