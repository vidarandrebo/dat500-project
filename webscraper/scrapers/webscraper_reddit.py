from requests_html import HTMLSession, AsyncHTMLSession
import asyncio
import time

def get_comment_links(s: HTMLSession, url: str) -> list:
    print("fetching posts...")
    r = s.get(url)
    r.html.render(scrolldown=50, sleep=1)
    articles = r.html.find('#AppRouter-main-content .scrollerItem')
    links = []
    for article in articles:
        check_reddit_link(links, article.links)
    return links

def check_reddit_link(links: list, article_links: list) -> list:
    for link in article_links:
        if len(link) > 3 and link[:3] == "/r/":
            links.append(link)
    return links

async def get_article(s: AsyncHTMLSession, article_url: str) -> str:
    print("-> fetching post...")
    url = f"https://www.reddit.com{article_url}"
    r = await s.get(url)
    title = r.html.find('div[data-adclicklocation="title"]', first=True)
    content = r.html.find('div[data-click-id="text"]', first=True)
    date = r.html.find('span[data-click-id="timestamp"]', first=True)
    res = ""
    try:
        title_text = title.text 
    except Exception as e:
        title_text = "" 
    try:
        date_text = date.text
    except Exception as e:
        date_text = ""
    try:
        res = format_article(title_text, content.text, date_text)
    except Exception as e:
        print(e)
    return res

def format_article(title: str, content: str, date: str) -> str:
    res = "DATE SCRAPED: " + str(time.ctime(time.time())) 
    res += "\nPOSTED: " + date
    res += "\nTITLE: " + title
    res += "\nCONTENT:\n" + content
    res += "\nEND CONTENT\n"
    return res

async def main(links: list) -> list:
    asession = AsyncHTMLSession()
    tasks = (get_article(asession, link) for link in links)
    return await asyncio.gather(*tasks)

def scrape_reddit():
    print("scraping reddit...")
    try:
        start = time.time()
        url = "https://www.reddit.com/r/stocks/new/"
        s = HTMLSession()
        urls = get_comment_links(s, url)
        mid = time.time()
        result = asyncio.run(main(urls))
        file_path = f"./files/reddit_results{str(round(time.time()))}.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("-----\n".join(result))
        end = time.time()
        print(f"\nElapsed (all): {round(end - start)} s")
        print(f"- Elapsed (get links): {round(mid - start)} s")
        print(f"- Elapsed (visit links): {round(end - mid)} s")

    except Exception as e:
        print(e)

if __name__ == "__main__":
    scrape_reddit()    