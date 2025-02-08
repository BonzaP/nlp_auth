from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import pandas as pd
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# chrome_path = r"driver/chromedriver.exe"
# s = Service(chrome_path)
#Golden City Hotel
#url = 'https://www.google.com/travel/search?q=%CE%B1%CE%B8%CE%B7%CE%BD%CE%B1&gsas=1&ts=CAESCgoCCAMKAggDEAAaWgo8EjgKBy9tLzBuMnoyJTB4MTRhMWJkMWYwNjcwNDNmMToweDI3MzYzNTQ1NzY2NjhkZGQ6BkF0aGVucxoAEhoSFAoHCOkPEAEYExIHCOkPEAEYFBgBMgIIAioRCgsoDToDRVVSYgIIARoAKAc&hl=en-GR&qs=CAESBENCST0yJkNoZ0kxWmVDaU91b2hkdUNBUm9MTDJjdk1YUm1jR3hmYmpJUUFROA1IAA&ap=KigKEglT3WlX9PhCQBGpZwgXqbQ3QBISCfeo-EinAENAEalnCHewxTdAMAC6AQdyZXZpZXdz'
#queenolga
#vergina thessaloniki
#url = 'https://www.google.com/travel/search?q=vergina%20thessaloniki&gsas=1&ts=CAESCAoCCAMKAggD&qs=CAAgASgA&ap=KigKEgl2iuqV_LRCQBFdsa4owVU5QBISCa5-2gtwtUJAEV2xrljMVjlAMAC6AQdyZXZpZXdz&biw=1920&bih=953&hl=en-GR'
#nammos mykonos
#url = 'https://www.google.com/travel/search?gsas=1&ts=EggKAggDCgIIAxocEhoSFAoHCOkPEAUYGxIHCOkPEAUYHBgBMgIQAA&qs=MhNDZ29JMjhXd3BLWDcwYThpRUFFOAI&ap=ugEHcmV2aWV3cw&biw=1920&bih=953&hl=en-GR&ved=0CAAQ5JsGahcKEwjY6aDAyv-KAxUAAAAAHQAAAAAQDA'
#candia hotel
#url = 'https://www.google.com/travel/search?q=%CE%B1%CE%B8%CE%B7%CE%BD%CE%B1&gsas=1&ts=CAESCgoCCAMKAggDEAAaWgo8EjgKBy9tLzBuMnoyJTB4MTRhMWJkMWYwNjcwNDNmMToweDI3MzYzNTQ1NzY2NjhkZGQ6BkF0aGVucxoAEhoSFAoHCOkPEAEYExIHCOkPEAEYFBgBMgIIAioRCgsoDToDRVVSYgIIARoAKAc&hl=en-GR&qs=CAESBENDUT0yJkNoZ0k2TEw0MWNhYTlyaExHZ3d2Wnk4eGFHUmZNR0p1ZUcwUUFROA1IAA&ap=KigKEglT3WlX9PhCQBGpZwgXqbQ3QBISCfeo-EinAENAEalnCHewxTdAMAC6AQdyZXZpZXdz'
#brittania international hotel london
url = 'https://www.google.com/travel/search?gsas=1&ts=EggKAggDCgIIAxocEhoSFAoHCOkPEAEYExIHCOkPEAEYFBgBMgIQAA&qs=MhNDZ29JMTYycW5xN2V2djF0RUFFOAI&ap=ugEHcmV2aWV3cw&biw=1920&bih=953&hl=en-GR&ved=0CAAQ5JsGahcKEwjog6CpgoCLAxUAAAAAHQAAAAAQDg'
driver = uc.Chrome()
driver.get(url)
action = ActionChains(driver)
#accept cookies popup
try:
    driver.find_element(By.XPATH, "//span[text() = 'Accept all']").click()
    time.sleep(2)
except:
    pass


#loading many reviews from the page by scrolling to the bottom until we cant scroll more

prev_height = -1
max_scrolls = 500
scroll_count = 0
body = driver.find_element(By.TAG_NAME, 'body')
while scroll_count < max_scrolls:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    body.send_keys(Keys.PAGE_UP)
    time.sleep(2)  # give some time for new results to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == prev_height:
        break
    prev_height = new_height
    scroll_count += 1

driver.execute_script("window.scrollTo(0, 0)")


#gathering ratings and reviews
df = pd.DataFrame(columns=['review', 'rating'])
reviews = driver.find_elements(By.XPATH, "//div[@class = 'Svr5cf bKhjM']")
for review_wrapper in reviews:
    rating_element = review_wrapper.find_element(By.XPATH, ".//div[@class = 'GDWaad']")
    driver.execute_script("arguments[0].scrollIntoView({ block: 'center' });", rating_element)
    driver.execute_script("window.scrollBy(0, 150)")
    #time.sleep(0.5)
    try:
        review_wrapper.find_element(By.XPATH, ".//span[text() = 'Read more']").click()
        time.sleep(0.5)
        review = review_wrapper.find_elements(By.XPATH, ".//div[@class = 'K7oBsc']//span")[2]
    except:
        review = review_wrapper.find_element(By.XPATH, ".//div[@class = 'K7oBsc']")
    review_text = review.text.replace("(Translated by Google)", "").split("(Original)")[0]
    review_text = review_text.replace("\n", "").lower()
    review_text = re.sub(r'[^\w\s]', '', review_text)
    review_text = re.sub(r'\d+', '', review_text)
    rating = rating_element.text
    if len(review_text):
        df.loc[len(df)] = [review_text, rating]

#saving dataframe as csv
df.to_csv('datasets/candia-hotel-only-google.csv')
driver.quit()
