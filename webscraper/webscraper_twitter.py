from requests_html import HTMLSession, AsyncHTMLSession
import asyncio
import time

def get_comment_links(s: HTMLSession, url: str) -> list:
    r = s.get(url)
    r.html.render(scrolldown=10,sleep=10)
    tweets = r.html.find('section[role="region"]')
    return [tweet.text for tweet in tweets]


if __name__ == "__main__":
    url = "https://twitter.com/elonmusk"
    s = HTMLSession()
    tweets = get_comment_links(s, url)
    print(tweets)
    with open("results2.txt", "w", encoding="utf-8") as file:
        file.write("\n---\n".join(tweets))
