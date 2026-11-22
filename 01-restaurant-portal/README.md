# Restaurant portal

This is the KodeFood back office. A restaurant adds dish photos, types the name of each photo, and sends the batch to the menu team. The team reviews the photos by hand and updates the customer menu within 24 hours.

Sample photos live in the repo `images/` folder. The portal reads them from there.

## Run it

```bash
cd 01-restaurant-portal
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:8000

## What to click

1. Pick a sample photo, or upload your own.
2. Write the name of that photo.
3. Choose **Add to this update**. Repeat for each dish.
4. Choose **Update our menu**.

The page then says someone from the menu team will review the photos and update the menu within 24 hours. **Start another update** clears the desk so you can run it again.
