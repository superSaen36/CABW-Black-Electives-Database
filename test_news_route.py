#!/usr/bin/env python3
"""
Test the news route logic to see if articles are being retrieved properly
"""

from fire_store_client import get_all_articles, get_approved_articles

print("="*80)
print("TESTING NEWS ROUTE LOGIC")
print("="*80)

# Simulate non-admin user
print("\n1. Testing PUBLIC VIEW (non-admin):")
print("-"*80)
all_articles = get_approved_articles()
print(f"Total approved articles: {len(all_articles)}")

if all_articles:
    featured_article = all_articles[0]
    news_entries = all_articles[1:3] if len(all_articles) > 1 else []

    print(f"\nFEATURED ARTICLE:")
    print(f"  Title: {featured_article.get('title')}")
    print(f"  Published: {featured_article.get('published')}")
    print(f"  Source: {featured_article.get('source')}")

    print(f"\nRECENT STORIES ({len(news_entries)} articles):")
    for i, article in enumerate(news_entries, 1):
        print(f"  {i}. {article.get('title')}")
        print(f"     Published: {article.get('published')}")
        print(f"     Source: {article.get('source')}")
else:
    print("⚠️  No approved articles found!")

# Simulate admin user
print("\n\n2. Testing ADMIN VIEW:")
print("-"*80)
all_articles_admin = get_all_articles()
print(f"Total articles (all): {len(all_articles_admin)}")

if all_articles_admin:
    featured_article = all_articles_admin[0]
    news_entries = all_articles_admin[1:3] if len(all_articles_admin) > 1 else []

    print(f"\nFEATURED ARTICLE:")
    print(f"  Title: {featured_article.get('title')}")
    print(f"  Approved: {featured_article.get('approved')}")

    print(f"\nRECENT STORIES ({len(news_entries)} articles):")
    for i, article in enumerate(news_entries, 1):
        print(f"  {i}. {article.get('title')}")
        print(f"     Approved: {article.get('approved')}")

print("\n" + "="*80)
print("✓ Test complete")
print("="*80)
