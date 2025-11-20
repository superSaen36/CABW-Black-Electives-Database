#!/usr/bin/env python3
"""
Script to add two more articles for the recent stories section.
"""

from fire_store_client import add_article

# Article 1
print("Adding article 1...")
article_id_1 = add_article(
    title="Barbara Lee Champions Federal Housing Bill in Congress",
    link="https://www.sfchronicle.com/politics/article/barbara-lee-housing-bill",
    published="November 13, 2025",
    source="San Francisco Chronicle",
    approved=True
)
print(f"✓ Article 1 added with ID: {article_id_1}")

# Article 2
print("\nAdding article 2...")
article_id_2 = add_article(
    title="Sydney Kamlager-Dove Leads Environmental Justice Initiative",
    link="https://www.latimes.com/california/story/2024-11-12/kamlager-dove-environmental-justice",
    published="November 12, 2025",
    source="Los Angeles Times",
    approved=True
)
print(f"✓ Article 2 added with ID: {article_id_2}")

print("\n" + "="*80)
print("✓ Successfully added 2 articles to Recent Stories section!")
print("="*80)
