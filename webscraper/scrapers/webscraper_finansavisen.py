from requests_html import HTMLSession, AsyncHTMLSession
import asyncio
import time

def get_latest_news(s: HTMLSession, url: str) -> list:
    r = s.get(url)
    r.html.render(sleep=3)
    articles = r.html.find('div[data-testid="Aksjeanalyse"]')
    articles.extend(r.html.find('div[data-testid="Markedskommentarer"]'))
    articles.extend(r.html.find('div[data-testid="Finans"]'))
    articles.extend(r.html.find('div[data-testid="Teknologi"]'))
    articles.extend(r.html.find('div[data-testid="Shipping"]'))
    articles.extend(r.html.find('div[data-testid="Olje"]'))
    articles.extend(r.html.find('div[data-testid="Sjømat"]'))
    articles.extend(r.html.find('div[data-testid="Luftfart"]'))
    articles.extend(r.html.find('div[data-testid="Næringseiendom"]'))
    links = []
    for article in articles:
        check_finansavsisen_links(links, article.links)
    return links

def check_finansavsisen_links(links: list, article_links: list) -> list:
    for link in article_links:
        if len(link) > 28 and link[:28] == "https://www.finansavisen.no/":
            links.append(link)
    return links

async def get_article(s: AsyncHTMLSession, article_url: str) -> str:
    url = article_url
    print(url)
    r = await s.get(url)
    title = r.html.find('h1[class="c-article-regular__title"]', first=True)
    date = r.html.find('div[class="c-article-regular__datetime"]', first=True)
    content = r.html.find('h2[class="c-article-regular__body__preamble"]', first=True)
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

def scrape_finansavisen():
    print("scraping finansavisen...")
    try:
        start = time.time()
        url = "https://bors.finansavisen.no/NOt=#quotelist"
        s = HTMLSession()
        urls = get_latest_news(s, url)
        mid = time.time()
        result = asyncio.run(main(urls))
        file_path = f"./webscraper/files/finansavisen_results{str(round(time.time()))}.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("-----\n".join(result))
        end = time.time()
        print(f"\nElapsed (all): {round(end - start)} s")
        print(f"- Elapsed (get links): {round(mid - start)} s")
        print(f"- Elapsed (visit links): {round(end - mid)} s")
    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    scrape_finansavisen()    