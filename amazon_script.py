from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import mysql.connector
from mysql.connector import Error
import time


#intializing chrome options and passing it into driver
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.amazon.com/')
time.sleep(3)

product = input("Enter Product name you want to search:")
print("Searching for {}".format(product))

def searching_product(product):
    search_element = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
    search_element.clear()
    search_element.send_keys(product)
    search_element.send_keys(Keys.RETURN)

def get_content():
    try:
        driver.implicitly_wait(7)

        title = driver.find_element_by_xpath('//*[@id="productTitle"]').text

        time.sleep(3)

        img_url = driver.find_element_by_xpath('//*[@id="landingImage"]').get_attribute('src')

        time.sleep(3)

        price = driver.find_element_by_xpath('//*[@id="priceblock_ourprice"]').text

        time.sleep(3)

        description_list = driver.find_elements_by_css_selector('#feature-bullets > ul > li > span')
        d_list = [x.text for x in description_list]
        para = " ".join(d_list)
        return [title, img_url, price, para]
    except:
        pass


def writing_into_database(content):
    try:
        mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'amazon_scrap'
        )
        cursor = mydb.cursor()
        sql = ("INSERT INTO shoes "
               "(title, img_url, price, para) "
               "VALUES (%s, %s, %s, %s)")
        cursor.execute(sql, content)
        mydb.commit()
        cursor.close()
        mydb.close()
    except:
        print("Some value can't be found")
        pass


def getting_links():
    try:
        time.sleep(5)
        products = driver.find_elements_by_css_selector('#search > div.sg-row > div.sg-col-20-of-24.sg-col-28-of-32.sg-col-16-of-20.sg-col.s-right-column.sg-col-32-of-36.sg-col-8-of-12.sg-col-12-of-16.sg-col-24-of-28 > div > span:nth-child(4) > div.s-result-list.s-search-results.sg-row > div > div > div > div > div:nth-child(2) > div:nth-child(2) > div > div.a-section.a-spacing-none.a-spacing-top-small > h2 > a')
        href_list = [x.get_attribute('href') for x in products]
        for i in href_list:
            driver.get(i)
            driver.implicitly_wait(15)
            content = get_content()
            time.sleep(5)
            writing_into_database(content)
    except:
        pass

searching_product(product)
getting_links()



