#!/usr/bin/env python3
"""
Test if the news page template would render correctly
"""

from app import app
from fire_store_client import get_approved_articles

# Simulate what the template would receive
approved_articles = get_approved_articles()

featured_article = approved_articles[0] if approved_articles else None
news_entries = approved_articles[1:3] if len(approved_articles) > 1 else []

print("="*80)
print("NEWS PAGE TEMPLATE DATA")
print("="*80)

print(f"\nFeatured Article Variable: {featured_article is not None}")
if featured_article:
    print(f"  Title: {featured_article.get('title')}")
    print(f"  Link: {featured_article.get('link')}")
    print(f"  Published: {featured_article.get('published')}")
    print(f"  Source: {featured_article.get('source')}")
else:
    print("  ⚠️  Featured article is None!")

print(f"\nNews Entries Variable: {len(news_entries)} articles")
for i, article in enumerate(news_entries, 1):
    print(f"  {i}. {article.get('title')}")

print("\n" + "="*80)
print("TEMPLATE CHECKS:")
print("="*80)
print(f"featured_article exists: {bool(featured_article)}")
print(f"news_entries exists and has items: {bool(news_entries and len(news_entries) > 0)}")
print("="*80)
