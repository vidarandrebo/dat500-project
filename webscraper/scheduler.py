import schedule
import time
from scrapers import webscraper_reddit, webscraper_twitter, webscraper_finansavisen, webscraper_cnbc, webscraper_dn, webscraper_fnlondon, webscraper_ft

schedule.every().day.at("00:00").do(webscraper_reddit.scrape_reddit)
schedule.every().day.at("01:00").do(webscraper_dn.scrape_dn)
schedule.every().day.at("02:00").do(webscraper_cnbc.scrape_cnbc)
schedule.every().day.at("03:00").do(webscraper_finansavisen.scrape_finansavisen)
schedule.every().day.at("04:00").do(webscraper_twitter.scrape_twitter)
schedule.every().day.at("05:00").do(webscraper_fnlondon.scrape_fnlondon)
schedule.every().day.at("06:00").do(webscraper_ft.scrape_ft)

timer = 0
sleep_time = 60
while True:
    if timer % 3600 == 0:
        print(str(time.ctime(time.time())))
    schedule.run_pending()
    time.sleep(sleep_time)
    timer += sleep_time