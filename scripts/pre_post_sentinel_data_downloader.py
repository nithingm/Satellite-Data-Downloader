#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pre_post_sentinel_data_downloader.py: Downloads Sentinel-2 pre- and post-event products using eodag.

Usage:
This code has only been tested on Linux.

    1. Install dependencies:
        pip install "eodag[copernicus]"
    2. Set environment variables:
        Create an account on Copernicus: https://dataspace.copernicus.eu/
        export EODAG__COP_DATASPACE__AUTH__CREDENTIALS__USERNAME="your_username(your email ID)"
        export EODAG__COP_DATASPACE__AUTH__CREDENTIALS__PASSWORD="your_password"

    3. The codebase contains sentinel products from Copernicus Browser for Mandalay, Myanmar. You can change it to whichever place you want to analyze. 
        a) Go to Copernicus Browser: https://browser.dataspace.copernicus.eu/ and login.
        b) Click on "SEARCH" tab (It will be on "VISUALISE" by default)
        c) If you know the product name (for the satellite images on a given date range), put the ID's directly. If not, go to the map on the right side and draw the AOI(Area of Interest) using the tools available on the right. You can use the "Go to Place" to make your searching easier.  
        d) Once this is ready, go to the "SEARCH" tab and click on "SENTINEL-2">"MSI">"L2A" and change cloud cover to your liking (I used 10% here). If using "L1C", be ready to preprocess the atmosphere and clouds away if required. I used only "L2A". No need to click on "Auxiliary Data File". 
        e) Put the pre-event dates and click search. Note the required product names. They look like this S2B_MSIL2A_20250327T035539_N0511_R004_T47QKV_20250327T073409(ignore the .SAFE part) and add them one by one to the 'list of products' variable: pre_event_products
        f)  Repeat the search for post-event dates and add them to the 'list of products' variable: post_event_products

    4. Run the script once you're in the main folder of the project:
        python scripts/pre_post_sentinel_data_downloader.py

    5. Products will be downloaded to:
        data/satellite/pre_event/sentinel_pre_event/
        data/satellite/post_event/sentinel_post_event/
      *Note: If the folders are not downloaded here(You can check these folders while downloading), it will be in /tmp on Linux based systems. 
        If it goes to /tmp download, navigate there (on the terminal, try 'cd /tmp') and look for a pattern in the beginning of the folder names and move it to the right folder using the following code:
        cp -r /tmp/<pattern>* <full directory you want to move it to>
        Example:
        cp -r /tmp/S2B_MSIL2A* ~/Desktop/MyanmarEarthquake/data/satellite/pre_event/sentinel_pre_event/
        Remember to handle this for pre and post-event separately!
"""

import os
import tqdm
from eodag import EODataAccessGateway


# ----- CONFIGURABLE SECTION (Just edit the lists below) -----
pre_event_products = [
    "S2B_MSIL2A_20250327T035539_N0511_R004_T47QKV_20250327T073409",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T46QHE_20250327T073409",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T47QLV_20250327T073409",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T47QLA_20250327T073409",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T47QLB_20250327T073409",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T47QMC_20250327T073409",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T47QKD_20250327T073409",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T46QHK_20250327T073409",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T47QLE_20250327T061954",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T47QME_20250327T073409",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T47QNE_20250327T061954",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T47QLF_20250327T061954",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T47QMF_20250327T061954",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T47QKG_20250327T061954",
    "S2B_MSIL2A_20250327T035539_N0511_R004_T47RLK_20250327T061954"
    # Change this list of products to the productID's you obtain from Copernicus Browser Search for the pre-event data
]

post_event_products = [
    "S2C_MSIL2A_20250401T035601_N0511_R004_T47QKV_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T46QHE_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T47QLV_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T47QLA_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T47QLB_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T47QMC_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T47QKD_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T46QHK_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T47QLE_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T47QME_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T47QNE_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T47QLF_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T47QMF_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T47QKG_20250401T091413",
    "S2C_MSIL2A_20250401T035601_N0511_R004_T47RLK_20250401T091413"
    # Change this list of products to the productID's you obtain from Copernicus Browser Search for the post-event data
]

product_type = "S2_MSI_L2A"
provider = "cop_dataspace"
output_dirs = {
    "pre": "data/satellite/pre_event/sentinel_pre_event",
    "post": "data/satellite/post_event/sentinel_post_event"
}
# -----------------------------------------------------------

def download_products(product_list, download_dir, label):
    print(f"\n=== Starting download: {label.upper()} ===")
    g = EODataAccessGateway()
    g.set_preferred_provider(provider)
    os.makedirs(download_dir, exist_ok=True)

    success, search_fail, download_fail = [], [], []

    for i, product_id in enumerate(tqdm(product_list, desc=f"[{label}] Downloading", unit="product")):
        print(f"\n[{label}] {i+1}/{len(product_list)}: {product_id}")
        try:
            results = g.search(provider=provider, productType=product_type, id=product_id)
            if not results:
                print(f"❌ Not found: {product_id}")
                search_fail.append(product_id)
                continue
            print(f"✅ Found: {results[0].properties.get('title', product_id)}")
            paths = g.download_all(results, download_root_dir=download_dir)
            if paths:
                print(f"✅ Downloaded to: {paths[0]}")
                success.extend(paths)
            else:
                print(f"❌ Download failed: {product_id}")
                download_fail.append(product_id)
        except Exception as e:
            print(f"❌ Error downloading {product_id}: {e}")
            download_fail.append(product_id)

    print(f"\n=== Summary for {label.upper()} ===")
    print(f"✅ Successful: {len(success)}")
    print(f"🔍 Not found: {len(search_fail)}")
    print(f"📥 Failed downloads: {len(download_fail)}")
    if search_fail:
        print("Not found:", search_fail)
    if download_fail:
        print("Failed downloads:", download_fail)

if __name__ == "__main__":
    if not os.environ.get("EODAG__COP_DATASPACE__AUTH__CREDENTIALS__USERNAME") or not os.environ.get("EODAG__COP_DATASPACE__AUTH__CREDENTIALS__PASSWORD"):
        print("❌ Missing COP_DATASPACE credentials in environment variables.")
        print("Please set EODAG__COP_DATASPACE__AUTH__CREDENTIALS__USERNAME and PASSWORD.")
        exit(1)

    download_products(pre_event_products, output_dirs["pre"], "pre_event")
    download_products(post_event_products, output_dirs["post"], "post_event")
    print("\n🎉 All downloads completed.")