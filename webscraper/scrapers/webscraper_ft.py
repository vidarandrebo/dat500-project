from requests_html import HTMLSession, AsyncHTMLSession
import asyncio
import time

def get_latest_news(s: HTMLSession, url: str) -> list:
    r = s.get(url)
    r.html.render(sleep=3)
    articles = r.html.find('ul li[class="o-teaser-collection__item o-grid-row"]')
    article_texts = []
    for article in articles:
        try:
            article_texts.append(article.text)
        except Exception as e:
            print(e)
    return article_texts

def scrape_ft():
    print("scraping ft...")
    try:
        start = time.time()
        result = []
        for no in range(1, 5):
            url = f"https://www.ft.com/markets?page={no}"
            s = HTMLSession()
            result.extend(get_latest_news(s, url))
        
        file_path = f"./files/ft_results{str(round(time.time()))}.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(result))
        end = time.time()
        print(f"\nElapsed (all): {round(end - start)} s")

    except Exception as e:
        print(e)

if __name__ == "__main__":
    scrape_ft()