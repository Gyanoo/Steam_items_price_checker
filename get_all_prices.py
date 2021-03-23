from time import sleep
import sticker_to_link_dict as sd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import re

def get_all_prices():
    driver = webdriver.Firefox()
    stickers_dict = sd.stickers_dict_all
    total_price = 0.0
    to_check = len(stickers_dict)
    checked = 0
    for sticker_name in stickers_dict.keys():
        link = get_link(sticker_name)
        driver.get(link)
        try:
            price_text = driver.find_element_by_class_name("normal_price").text
        except NoSuchElementException:
            while driver.find_elements_by_id("message") and driver.find_element_by_id("message").text[0:6] == "Sorry!":
                print("To many requests! Retrying in 60 seconds...")
                sleep(60)
                print("Retrying...")
                driver.get(link)
        finally:
            price_text = driver.find_element_by_class_name("normal_price").text
            print(price_text)
            price = float(format(float((re.split(" ", price_text)[2][1:]).replace(',', '')), '.2f'))
            stickers_dict[sticker_name].append(price)
            checked += 1
            print("checked " + str(checked) + " out of " + str(to_check))
            total_price += float(format(stickers_dict[sticker_name][0] * price, '.2f'))
    driver.quit()
    return stickers_dict, str(total_price)


def get_link(sticker_name):
    link_base = "https://steamcommunity.com/market/search?appid=730&q="
    search_query = sticker_name.replace(" ", "+")
    return link_base + search_query
