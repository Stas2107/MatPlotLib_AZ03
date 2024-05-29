import time
import csv
import re
import matplotlib.pyplot as plt
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

    # Использование регулярных выражений для фильтрации только числовых значений
    numeric_price = re.findall(r'\d+', price.replace(' ', ''))
    if numeric_price:
        numeric_price = ''.join(numeric_price)  # Объединяем список цифр в строку
        data.append([numeric_price])

# Закрытие браузера
browser.quit()

# Сохранение данных в CSV файл
with open('prices.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Price'])  # Заголовок столбца
    writer.writerows(data)

print("Data has been saved to prices.csv")

# Найти среднюю цену
numeric_prices = [int(price[0]) for price in data]
average_price = sum(numeric_prices) / len(numeric_prices)
print(f"Средняя цена: {average_price:.2f} руб.")

# Построить гистограмму цен
plt.hist(numeric_prices, bins=20, edgecolor='black')
plt.title('Гистограмма цен на диваны')
plt.xlabel('Цена (рубли)')
plt.ylabel('Количество')
plt.grid(True)
plt.show()