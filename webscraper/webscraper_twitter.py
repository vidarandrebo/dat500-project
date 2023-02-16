from requests_html import HTMLSession, AsyncHTMLSession
import asyncio
import time

def get_comment_links(s: HTMLSession, url: str) -> list:
    t1 = time.time()
    r = s.get(url)
    t2 = time.time()
    r.html.render(scrolldown=10,sleep=5)
    t3 = time.time()
    tweets = r.html.find('section[role="region"]')
    t4 = time.time()

    print(f"t2-t1: {round(t2 - t1)} s")
    print(f"t3-t2: {round(t3 - t2)} s")
    print(f"t4-t3: {round(t4 - t3)} s")

    return [tweet.text for tweet in tweets]


if __name__ == "__main__":
    start = time.time()
    url = "https://twitter.com/elonmusk"
    s = HTMLSession()
    tweets = get_comment_links(s, url)
    with open("results2.txt", "w", encoding="utf-8") as file:
        file.write("\n---\n".join(tweets))
    end = time.time()
    print(f"\nElapsed: {round(end - start)} s")

