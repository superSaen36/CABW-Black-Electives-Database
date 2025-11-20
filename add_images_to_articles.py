#!/usr/bin/env python3
"""
Script to add placeholder images to our custom articles
"""

from fire_store_client import update_document_by_id

# Sample images for our articles (using unsplash placeholder images)
articles_with_images = [
    {
        "id": "T5Jmlp5mqB6UWEPEGpgm",  # Karen Bass
        "title": "Karen Bass Announces Major Housing Initiative for Los Angeles",
        "image_url": "https://images.unsplash.com/photo-1449844908441-8829872d2607?w=800&h=600&fit=crop"
    },
    {
        "id": "cJmtu5mqNTQIVWDOMRPR",  # Barbara Lee
        "title": "Barbara Lee Champions Federal Housing Bill in Congress",
        "image_url": "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800&h=600&fit=crop"
    },
    {
        "id": "BFwPva6xcg6680r5YN5H",  # Sydney Kamlager-Dove
        "title": "Sydney Kamlager-Dove Leads Environmental Justice Initiative",
        "image_url": "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=800&h=600&fit=crop"
    }
]

print("="*80)
print("ADDING IMAGES TO CUSTOM ARTICLES")
print("="*80)

for article in articles_with_images:
    print(f"\nUpdating: {article['title']}")
    print(f"  ID: {article['id']}")
    print(f"  Image: {article['image_url']}")

    success = update_document_by_id(
        collection="articles",
        doc_id=article['id'],
        data={"image_url": article['image_url']}
    )

    if success:
        print(f"  ✓ Image added successfully")
    else:
        print(f"  ✗ Failed to add image")

print("\n" + "="*80)
print("✓ Done! Images have been added to custom articles.")
print("="*80)
print("\nRestart your Flask app to see the images on the news page!")
