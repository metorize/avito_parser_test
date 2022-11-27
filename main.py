from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import datetime

product_name = input("Enter product_name: ")
product_amount = int(input("How many: "))
dic_response = {
    "search": product_name,
    "result": [

    ]
}
# options
options = webdriver.ChromeOptions()

# user-agent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0")

# for ChromeDriver version 79.0.3945.16 or over
options.add_argument("--disable-blink-features=AutomationControlled")


# headless mode
options.headless = True

def pubdate_correct(pubdate):
    months = {
        "января": 1,
        "февраля": 2,
        "марта": 3,
        "апреля": 4,
        "мая": 5,
        "июня": 6,
        "июля": 7,
        "августа": 8,
        "сентября": 9,
        "октября": 10,
        "ноября": 11,
        "декабря": 12,
    }
    if pubdate[0] in "св":
        if pubdate[0] == 'с':
            date = datetime.date.today()
        elif pubdate[0] == 'в':
            date = datetime.date.today() - datetime.timedelta(days=1)
        string_date = date.strftime("%Y-%m-%d")
        return string_date
    else:
        date_array = pubdate.split()
        day = date_array[0]
        month = months[date_array[1]]
        date = datetime.date(2022, month, int(day))
        string_date = date.strftime("%Y-%m-%d")
        return string_date



driver = webdriver.Chrome(options=options)
count = 0

try:
    driver.get(f"https://www.avito.ru/moskva?q={product_name}")

    driver.implicitly_wait(5)

    items = driver.find_elements(By.XPATH, "//div[@data-marker='item-photo']")

    for item in items:
        count += 1
        if count > product_amount:
            break
        item.click()
        # print(driver.window_handles)

        # time.sleep(5)
        driver.implicitly_wait(5)

        driver.switch_to.window(driver.window_handles[1])
        #
        # time.sleep(5)
        driver.implicitly_wait(5)
        # Title:
        product = driver.find_element(By.CLASS_NAME, "title-info-title-text").text
        # Description
        description = driver.find_element(By.CLASS_NAME, "style-item-description-pL_gy").text
        # print(description.text)
        # Url:
        url = driver.current_url
        # Price:
        try:
            price = driver.find_element(By.CLASS_NAME, "style-item-price-text-_w822").text
        except:
            price = "Price not specified"
        # Date
        pubdate = driver.find_element(By.XPATH, "//span[@data-marker='item-view/item-date']").text[2:]
        driver.implicitly_wait(5)
        dic_result = {
            "title": product,
            "desc": description,
            "url": url,
            "price": price,
            "pubDate": pubdate_correct(pubdate),
        }
        driver.close()
        dic_response['result'].append(dic_result)
        driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.window(driver.window_handles[0])
except Exception as ex:
    print(ex)
finally:
    driver.quit()
    # driver.close()
    print(dic_response)
    with open(f"{product_name}.json", "w", encoding="utf-8") as file:
        json.dump(dic_response, file, indent=4, ensure_ascii=False)
