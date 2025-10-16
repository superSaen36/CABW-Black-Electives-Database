
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
            # else:
            #     data["published"] = ""
            print("-" * 20)
            entries.append(data)
    return entries
        
# get_feed_data()