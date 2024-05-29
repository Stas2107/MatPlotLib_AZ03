import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Функция для отладки
def debug_message(message):
    print(f"[DEBUG] {message}")

try:
    # Настройка Selenium Chrome
    options = Options()
    options.add_argument("--headless")  # Запуск Chrome в фоновом режиме
    options.add_argument("--disable-gpu")  # Отключение GPU (может помочь при запуске в фоновом режиме)
    options.add_argument("--no-sandbox")  # Отключение песочницы (может помочь при запуске в некоторых системах)
    service = Service(ChromeDriverManager().install())

    debug_message("Запуск браузера...")
    driver = webdriver.Chrome(service=service, options=options)

    # URL страницы
    url = "https://www.divan.ru/category/divany-i-kresla"
    debug_message(f"Переход на страницу: {url}")
    driver.get(url)
    time.sleep(5)  # Ждем, пока страница полностью загрузится

    # Парсинг данных
    debug_message("Начало парсинга данных...")
    products = driver.find_elements(By.CLASS_NAME, 'product-card-wrapper')

    data = []
    for product in products:
        try:
            title = product.find_element(By.CLASS_NAME, 'product-card__title').text
        except:
            title = "N/A"

        try:
            price = product.find_element(By.CLASS_NAME, 'product-card__price-current').text
        except:
            price = "N/A"

        data.append([title, price])

    # Закрытие браузера
    debug_message("Закрытие браузера...")
    driver.quit()

    # Сохранение данных в CSV файл
    debug_message("Сохранение данных в CSV файл...")
    header = ['Title', 'Price']
    with open('divan_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    print("Данные сохранены в файл divan_data.csv")
except Exception as e:
    print(f"Произошла ошибка: {e}")