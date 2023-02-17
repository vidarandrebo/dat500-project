from requests_html import HTMLSession, AsyncHTMLSession
import asyncio
import time

def get_latest_news(s: HTMLSession, url: str) -> list:
    r = s.get(url)
    r.html.render(sleep=3)
    articles = r.html.find('article')
    links = []
    for article in articles:
        check_dn_links(links, article.links)
    return links

def check_dn_links(links: list, article_links: list) -> list:
    for link in article_links:
        if len(link) > 25 and link[:25] == "https://www.fnlondon.com/":
            links.append(link)
    return links

async def get_article(s: AsyncHTMLSession, article_url: str) -> str:
    url = article_url
    print(url)
    r = await s.get(url)
    title = r.html.find('h1[itemprop="headline"]', first=True)
    date = r.html.find('time[datetime]', first=True)
    content = r.html.find('div[class="fn-snippet-body"]', first=True)
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
        content_text = content.text
    except Exception as e:
        content_text = ""
    if content_text == "" and title_text == "":
        return ""
    try:
        res = format_article(title_text, content_text, date_text)
    except Exception as e:
        print(e)
    return res

def format_article(title: str, content: str, date: str) -> str:
    res = "DATE: " + str(time.ctime(time.time())) + "\nPOSTED: " + date
    res += "\nTITLE: " + title
    res += "\nCONTENT:\n" + content
    res += "\nEND CONTENT\n"
    return res

async def main(links: list) -> list:
    asession = AsyncHTMLSession()
    tasks = (get_article(asession, link) for link in links)
    return await asyncio.gather(*tasks)

def scrape_fnlondon():
    print("scraping fnlondon...")
    try:
        start = time.time()
        urls = []
        for no in range(1, 5):
            url = f"https://www.fnlondon.com/investment-banking/{no}"
            s = HTMLSession()
            urls.extend(get_latest_news(s, url))
        
        mid = time.time()
        result = asyncio.run(main(urls))
        file_path = f"./webscraper/files/fnlondon_results{str(round(time.time()))}.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("-----\n".join(result))
        end = time.time()
        print(f"\nElapsed (all): {round(end - start)} s")
        print(f"- Elapsed (get links): {round(mid - start)} s")
        print(f"- Elapsed (visit links): {round(end - mid)} s")

    except Exception as e:
        print(e)

if __name__ == "__main__":
    scrape_fnlondon()