
import feedparser

feed_list = [
"https://lao.ca.gov/laoapp/rss/LAORSSFeedNew.aspx?laofeed=21",
"https://votesmart.org/rss/key-votes/CA",
"https://capitolweekly.net/feed/",
"https://advocacy.calchamber.com/feed/",
"https://www.govinfo.gov/rss/uscourts-casd.xml"
]

"""
NO data from:
    READING FROM https://www.sos.ca.gov/administration/multimedia/available-rss-feeds
    READING FROM https://lao.ca.gov/RSS
    READING FROM https://legiscan.com/rss
    READING FROM https://votesmart.org/media/rss
    READING FROM https://www.govinfo.gov/feeds
    READING FROM https://temeculaca.gov/rss.aspx
    READING FROM https://www.herculesca.gov/i-want-to/advanced-components/list-all-rss-feed

Recieving data from:
    READING FROM https://capitolweekly.net/feed/

"""


# print(f"Feed Title: {feed.feed.title}")
# print(f"Feed Link: {feed.feed.link}")
# print(f"Feed Description: {feed.feed.description}\n")
def get_feed_data():
    entries = []
    for feed_url in feed_list:
        feed = feedparser.parse(feed_url)
        print("READING FROM", feed_url)
        for entry in feed.entries:
            data = {}  # Create a new dictionary for each entry
            print(f"Title: {entry.title}")
            data["title"] = entry.title
            print(f"Link: {entry.link}")
            data["link"] = entry.link
            # if instance('FeedParserDict',):
            print(f"Published: {entry.published}")
            data["published"] = entry.published

            # Extract image from various possible sources
            image_url = None

            # Try media:content (common in RSS feeds)
            if hasattr(entry, 'media_content') and entry.media_content:
                image_url = entry.media_content[0].get('url')

            # Try media:thumbnail
            elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                image_url = entry.media_thumbnail[0].get('url')

            # Try enclosures (podcast/media attachments)
            elif hasattr(entry, 'enclosures') and entry.enclosures:
                for enclosure in entry.enclosures:
                    if enclosure.get('type', '').startswith('image/'):
                        image_url = enclosure.get('href')
                        break

            # Try description for img tags
            elif hasattr(entry, 'description'):
                import re
                img_match = re.search(r'<img[^>]+src="([^"]+)"', entry.description)
                if img_match:
                    image_url = img_match.group(1)

            # Try content for img tags
            elif hasattr(entry, 'content') and entry.content:
                import re
                img_match = re.search(r'<img[^>]+src="([^"]+)"', entry.content[0].value)
                if img_match:
                    image_url = img_match.group(1)

            data["image_url"] = image_url
            if image_url:
                print(f"Image: {image_url}")

            # else:
            #     data["published"] = ""
            print("-" * 20)
            entries.append(data)
    return entries
        
# get_feed_data()