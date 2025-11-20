#!/usr/bin/env python3
"""
Script to add a featured article to the news page.
"""

from fire_store_client import add_article
from datetime import datetime

# Featured article data
title = "Karen Bass Announces Major Housing Initiative for Los Angeles"
link = "https://www.latimes.com/california/story/2024-11-14/karen-bass-housing-initiative"
published = "November 14, 2025"
source = "Los Angeles Times"
approved = True

print("Adding featured article...")
print(f"Title: {title}")
print(f"Link: {link}")
print(f"Published: {published}")
print(f"Source: {source}")

# Add the article to Firestore
article_id = add_article(
    title=title,
    link=link,
    published=published,
    source=source,
    approved=approved
)

print(f"\n✓ Featured article added successfully with ID: {article_id}")
print("The article will appear in the Featured Story section on the news page.")
