from requests_html import HTMLSession, AsyncHTMLSession
import asyncio
import time

def get_comment_links(s: HTMLSession, url: str) -> str:
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

    scraped_time = str(time.ctime(time.time()))
    result = ["SCRAPED" + scraped_time]
    t = [tweet.text for tweet in tweets]
    result.extend(t)
    result.append("END SCRAPED:" + scraped_time)
    return result

def scrape_twitter():
    print("scraping twitter...")
    try:
        start = time.time()
        url = "https://twitter.com/elonmusk"
        s = HTMLSession()
        tweets = get_comment_links(s, url)
        file_path = f"./webscraper/files/twitter_results{str(round(time.time()))}.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n---\n".join(tweets))
        end = time.time()
        print(f"\nElapsed: {round(end - start)} s")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    scrape_twitter()
