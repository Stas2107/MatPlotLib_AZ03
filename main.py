import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Настройка Selenium Chrome
options = Options()
options.add_argument("--headless")  # Запуск Chrome в фоновом режиме
browser = webdriver.Chrome(options=options)  # добавляем options=options

# URL страницы
url = "https://www.divan.ru/category/divany-i-kresla"
browser.get(url)
time.sleep(5)  # Увеличим время ожидания до 5 секунд для полной загрузки страницы

# Парсинг данных
products = browser.find_elements(By.CLASS_NAME, 'LlPhw')

data = []
for product in products:
    try:
        # Использование CSS-селектора для получения цены
        price = product.find_element(By.CSS_SELECTOR, '[data-testid="price"]').text
    except:
        price = "N/A"

    # Логируем найденные данные для отладки
    print(f"Price: {price}")

    data.append([price])

# Закрытие браузера
browser.quit()

# Сохранение данных в CSV файл
header = ['Price']
with open('divan_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)

print("Данные сохранены в файл divan_data.csv")