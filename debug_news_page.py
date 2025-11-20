#!/usr/bin/env python3
"""
Debug script to check why articles aren't showing on news page
"""

from fire_store_client import get_all_articles, get_approved_articles

print("="*80)
print("DEBUGGING NEWS PAGE")
print("="*80)

# Test what the news route would see
print("\n1. Checking approved articles (what public users see):")
approved = get_approved_articles()
print(f"   Total approved articles: {len(approved)}")

if approved:
    print(f"\n   Featured article would be:")
    featured = approved[0]
    print(f"   - Title: {featured.get('title')}")
    print(f"   - ID: {featured.get('id')}")
    print(f"   - Approved: {featured.get('approved')}")
    print(f"   - Has all fields: title={bool(featured.get('title'))}, link={bool(featured.get('link'))}, published={bool(featured.get('published'))}")

    print(f"\n   Recent stories would be:")
    recent = approved[1:3] if len(approved) > 1 else []
    for i, article in enumerate(recent, 1):
        print(f"   {i}. {article.get('title')}")
else:
    print("   ⚠️  NO APPROVED ARTICLES FOUND!")

# Check all articles
print("\n2. Checking all articles:")
all_articles = get_all_articles()
print(f"   Total articles: {len(all_articles)}")
print(f"   First 3 articles:")
for i, article in enumerate(all_articles[:3], 1):
    print(f"   {i}. {article.get('title')} - Approved: {article.get('approved')}")

print("\n" + "="*80)
