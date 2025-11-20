#!/usr/bin/env python3
"""
Script to check articles in the database
"""

from fire_store_client import get_all_articles, get_approved_articles

print("="*80)
print("CHECKING ARTICLES IN DATABASE")
print("="*80)

# Get all articles
all_articles = get_all_articles()
print(f"\nTotal articles in database: {len(all_articles)}")

# Get approved articles
approved_articles = get_approved_articles()
print(f"Approved articles: {len(approved_articles)}")

if all_articles:
    print("\n" + "-"*80)
    print("ARTICLE DETAILS:")
    print("-"*80)
    for i, article in enumerate(all_articles, 1):
        print(f"\n{i}. {article.get('title', 'No title')}")
        print(f"   ID: {article.get('id', 'No ID')}")
        print(f"   Source: {article.get('source', 'No source')}")
        print(f"   Published: {article.get('published', 'No date')}")
        print(f"   Approved: {article.get('approved', False)}")
        print(f"   Link: {article.get('link', 'No link')}")
else:
    print("\n⚠️  No articles found in database!")
    print("\nThis means the articles may not have been added successfully.")
    print("Try running add_featured_article.py and add_more_articles.py again.")

print("\n" + "="*80)
