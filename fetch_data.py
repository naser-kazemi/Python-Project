import json
import os
import re
import time

import mysql.connector as db_connector
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def set_diver():
    chromedriver = '/usr/local/bin/chromedriver'
    ser = Service(chromedriver)
    op = webdriver.ChromeOptions()
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(service=ser, options=op)
    return driver


def get_houses():
    driver = set_diver()
    url = 'https://kilid.com/buy/tehran?locations=c_2301021576&subType=buy&type=listing&sort=date,DESC&utilId=1'
    driver.get(url)
    data = []
    for i in range(1, 200):
        driver.execute_script("window.scrollTo(1, 20)")
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, features='html.parser')
        data.extend(soup.find_all('div', attrs={'class': 'flex-col card-detail-holder'}))
    return data


def extract_data():
    data = get_houses()
    details = []
    for card in data:
        try:
            card = str(card)
            temp = dict()
            temp['price'] = re.findall(r'([\d.]+) میلیارد تومان', card)[0]
            temp['region'] = re.findall(r'</path></g></g></svg></i> ([\u0600-\u06FF -]+) </div>', card)[0]
            temp['area'] = re.findall(r'</g></svg></i> (\d+) متر </div>', card)[0]
            temp['room'] = re.findall(r'</g></svg></i> (\d+) خواب </div>', card)[0]
            temp['type'] = re.findall(r'</path></svg></i> ([\u0600-\u06FF]+) </div>', card)[0]
            details.append(temp)
        except IndexError:
            pass
    return details


def insert_into_database(data):
    try:
        cnx = db_connector.connect(user='root', password='naser2002ka', host='localhost', database='Practice',
                                   connect_timeout=1)
        cursor = cnx.cursor()
        for house in data:
            try:
                price = float(house['price'])
                house_type = house['type']
                area = int(house['area'])
                rooms = int(house['room'])
                region = house['region']
                add_data = "INSERT INTO house (type, area, room, region, price) VALUES('%s', '%d', '%d', '%s', '%.2f');" % (
                    house_type, area, rooms, region, price)
                cursor.execute(add_data)
                cnx.commit()
            except Exception as ex:
                print(ex)
        cursor.close()
        cnx.close()
        print('data was successfully fetched')
    except db_connector.Error as err:
        print(err)


def save_json_map(data):
    house_type = dict()
    region = dict()
    try:
        house_type = json.load(open('house_type.json', 'r'))
    except IOError:
        pass
    try:
        region = json.load(open('region.json', 'r'))
    except IOError:
        pass
    house_type_cnt = len(house_type) + 1
    region_cnt = len(region) + 1
    for card in data:
        try:
            if house_type.get(card['type']) is None:
                house_type[card['type']] = house_type_cnt
                house_type_cnt += 1
            if region.get(card['region']) is None:
                region[card['region']] = region_cnt
                region_cnt += 1
        except Exception as ex:
            print(ex)
    with open("house_type.json", "w") as outfile:
        json.dump(house_type, outfile)
    with open("region.json", "w") as outfile:
        json.dump(region, outfile)


def main():
    data = extract_data()
    insert_into_database(data)
    save_json_map(data)


if __name__ == '__main__':
    main()
