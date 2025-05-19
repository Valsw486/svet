import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Настройка драйвера
options = Options()
options.headless = True  # Запуск в фоновом режиме
driver = webdriver.Firefox(options=options)
url = "https://www.divan.ru/krasnodar/category/svet"

try:
    driver.get(url)
    # Ожидание загрузки элементов
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._Ud0k')))

    # Находим все элементы со светом
    divans = driver.find_elements(By.CSS_SELECTOR, 'div._Ud0k')

    # Подготовка для сохранения данных
    parsed_data = []

    # Извлечение данных о свете
    for divan in divans:
        try:
            name = divan.find_element(By.CSS_SELECTOR, 'div.lsooF span').text
            price = divan.find_element(By.CSS_SELECTOR, 'div.pY3d2 span').text
            link = divan.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

            parsed_data.append([name, price, link])
        except Exception as e:
            print(f"Произошла ошибка при парсинге: {e}")
            continue

finally:
    driver.quit()

# Сохранение данных в CSV файл
with open("divans.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название', 'Цена', 'Ссылка'])
    writer.writerows(parsed_data)

print("Данные успешно сохранены в divans.csv")
