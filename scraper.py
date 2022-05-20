from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from models import Apartment
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from models import ApartmentsDataWriter

ROW_LIMIT = 100
FILE_NAME = 'data'
WEBDRIVER_PATH = "your chromedriver path"


def create_driver():
    ser = Service(WEBDRIVER_PATH)
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    return driver


def start_scraping(url, file_name=FILE_NAME, row_limit=ROW_LIMIT):
    if len(file_name) == 0:
        file_name = FILE_NAME
    if row_limit is None or row_limit == 0:
        row_limit = ROW_LIMIT

    driver = create_driver()
    driver.get(url)
    current_row = 1

    all_data = []

    while current_row < row_limit:
        apartments = driver.find_elements(By.CLASS_NAME, 'card_params')
        for apartment in apartments:
            price_tag = apartment.find_element(By.CLASS_NAME, 'price')
            price_value = price_tag.find_element(By.CLASS_NAME, 'price-val').text
            price_value = "".join(price_value.split(' '))  # 12 000 -> 12000

            price_currency = price_tag.find_element(By.CLASS_NAME, 'price-cur').text

            location = apartment.find_element(By.CLASS_NAME, 'location').text

            list_tags = [tag.text for tag in apartment.find_elements(By.TAG_NAME, 'li')]
            room = list_tags[0]
            area = list_tags[1]
            floor = None if len(list_tags) < 3 else list_tags[2]

            if room:
                room = room.split(' ')[0]  # 2 otaqli -> 2
            if area:
                area = area.split(' ')[0]  # 5 m2 -> 5
            if floor:
                floor = floor.split(' ')[0].split('/')[0]  # 3/9 mertebe -> 3/9 -> 3

            apartment = Apartment(price_value, price_currency, location, room, area, floor)
            all_data.append(apartment)

            print('Row ', current_row, ': ', apartment.get_all_in_list())

            if current_row >= row_limit:
                break
            current_row += 1

        try:
            next_button = driver.find_element(By.LINK_TEXT, 'Növbəti')
            next_button.click()
            sleep(3)
        except NoSuchElementException:
            break

    data_writer = ApartmentsDataWriter(file_name, ['Price', 'Currency', 'Location', 'Room', 'Area', 'Floor'], all_data)
    data_writer.write()

    driver.quit()
