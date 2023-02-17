import schedule
import time

def test():
    print("This is a test. Should be printed every 10 seconds")

schedule.every(10).seconds.do(test)

timer = 0
sleep_time = 1
while True:
    print(timer)
    schedule.run_pending()
    time.sleep(sleep_time)
    timer += sleep_time