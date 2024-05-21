#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 14:48:40 2024

@author: james
"""


import cloudinary
import cloudinary.api
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configuration       
cloudinary.config( 
    cloud_name = "ddfqaz73q", 
    api_key = "431974138645946", 
    api_secret = "xs3XhQ2TUNCSrMg5-EUkYLveU-0", # Click 'View Credentials' below to copy your API secret
    secure=True
)

# Upload an image
upload_result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
                                           public_id="shoes")
print(upload_result["secure_url"])

# Optimize delivery by resizing and applying auto-format and auto-quality
optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")
print(optimize_url)

# Transform the image: auto-crop to square aspect_ratio
auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")
print(auto_crop_url)

public_ids = ["shoes"]

result = cloudinary.api.resource_by_asset_id(upload_result["asset_id"])
print(result)

image_delete_result = cloudinary.api.delete_resources(public_ids, resource_type="image", type="upload")
print(image_delete_result)