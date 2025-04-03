# Satellite Data Downloader
## Currently designed for the Myanmar Earthquake -March 28th 2025

This repo contains a clean, reproducible script to download **pre- and post-event Sentinel-2 imagery** from the [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) using the `eodag` Python library.

It was originally built to assess the impact of the 2025 Myanmar earthquake in Mandalay, but the workflow can be used for any location or time period by simply updating the product IDs.


Helps researchers and practitioners quickly fetch satellite data relevant for:

- Change detection (NDVI/NDBI)

- Urban damage mapping

- Disaster response and recovery studies

- Educational and geospatial tutorials

---

## 🚀 Features
- Download both **pre-event** and **post-event** satellite images in one run.
- Output folders automatically created:
  - `data/satellite/pre_event/sentinel_pre_event/`
  - `data/satellite/post_event/sentinel_post_event/`
- Designed for disaster monitoring (Current e.g., Mandalay, Myanmar earthquake).
- Easily extendable to **any location** by editing product ID lists.

---

## 🧰 Requirements
Tested on **Linux**. Should work on macOS too. Untested on Windows, but it should not be too different.
Make sure Python is installed.
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🔐 Authentication
1. **Create an account** at [Copernicus Data Space](https://dataspace.copernicus.eu/).
2. Export your credentials as environment variables:

```bash
export EODAG__COP_DATASPACE__AUTH__CREDENTIALS__USERNAME="your_email@example.com"
export EODAG__COP_DATASPACE__AUTH__CREDENTIALS__PASSWORD="your_password"
```

---

## 🌍 Get Product IDs from Copernicus Browser
These "Products" refer to satellite data chunks you can download from here
1. Go to [Copernicus Browser](https://browser.dataspace.copernicus.eu/).
2. Switch from **Visualise** to **Search** tab.
3. Use map tools to define an AOI (Area of Interest) or enter a location manually.
4. Filter by:
   - **DATA SOURCES**: Sentinel-2 ✅→ MSI ✅→ Level-2A (L2A) ✅
     (This is what I used. Feel free to use what you might find right for your use case)
   - **Cloud Cover**: Recommended < 20%. I used 10%.
5. Set date range before and after the event.
6. Copy the full product names (e.g. `S2B_MSIL2A_20250327T035539_N0511_R004_T47QKV_20250327T073409` — ignore the `.SAFE` part!) into these two variables:
   - `pre_event_products`
   - `post_event_products`

Edit these lists in [`pre_post_sentinel_data_downloader.py`](pre_post_sentinel_data_downloader.py).

---

## 📦 Run the Downloader
From the project root:
```bash
python pre_post_sentinel_data_downloader.py
```

Downloaded products will be saved in:
```
data/satellite/pre_event/sentinel_pre_event/
data/satellite/post_event/sentinel_post_event/
```

> **Note**: On some Linux systems, EODAG may download files to `/tmp` by default if a local directory isn't enforced.
>
> To fix this, manually move those files back into the right folder using a command like:
> ```bash
> cp -r /tmp/S2B_MSIL2A* ./data/satellite/pre_event/sentinel_pre_event/
> cp -r /tmp/S2C_MSIL2A* ./data/satellite/post_event/sentinel_post_event/
> ```
> You can inspect `/tmp` and copy files based on matching patterns. Make sure to move **pre** and **post** products separately.

---

## 📁 Folder Structure
```
├── pre_post_sentinel_data_downloader.py
├── .gitignore
├── requirements.txt
├── README.md
└── data
    └── satellite
        ├── pre_event
        │   └── sentinel_pre_event  ← images downloaded here
        └── post_event
            └── sentinel_post_event ← images downloaded here
```

---

## 📬 Contact
Built by [Nithin](https://github.com/nithingm) as part of a disaster analysis pipeline.

Feel free to fork, star, and collaborate! 🤝

