from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv

def parse_table_to_csv(headers, table_text_b, output_file):
    body = []
    for line in table_text_b.strip().split('\n'):
        parts = line.split()
        score = parts[-2].replace(',', '.')
        region = ' '.join(parts[1:-2]).strip().lower()
        region = region.replace('—', '-')
        body.append([region, score])

    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(headers)
        writer.writerows(body)


# Парс таблицы "Рейтинг регионов по приверженности населения ЗОЖ"
driver = webdriver.Chrome()

url = 'https://riarating.ru/infografika/20210927/630209338.html'
driver.get(url)

table_header = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'header-wrap--3_u7Y'))).text
table_body = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'body-wrap--1spEG'))).text

headers = table_header.split('\n')[1:-1]
headers[1] = 'Рейтинговый балл приверженности населения ЗОЖ'

parse_table_to_csv(headers, table_body, 'result_tables\\table_helth.csv')


# Парс таблицы "Рейтинг регионов РФ по финансовому благополучию населения"
driver = webdriver.Chrome()

url = 'https://riarating.ru/infografika/20211012/630210562.html'
driver.get(url)

table_header = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'header-wrap--3_u7Y'))).text
table_body = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'body-wrap--1spEG'))).text

headers = table_header.split('\n')[1:-1]
headers[1] = 'Рейтинговый балл финансового благополучия населения'

parse_table_to_csv(headers, table_body, 'result_tables\\table_finance.csv')

# Парс координат регионов
driver = webdriver.Chrome()

url = 'https://riarating.ru/infografika/20241223/630274686.html'
driver.get(url)

svg_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'svg[data-visible="true"]')))

regions = svg_element.find_elements(By.XPATH, './*')

region_positions = {}

for region in regions:
    data_name = region.get_attribute('data-name')
    
    rect_element = region.find_element(By.TAG_NAME, 'rect')
    text_element = region.find_element(By.TAG_NAME, 'text')

    rect_x = rect_element.get_attribute('x')
    rect_y = rect_element.get_attribute('y')

    region_name = data_name.strip().lower().replace('—', '-')
    x_y_list = [int(rect_x), int(rect_y)]

    region_positions[region_name] = x_y_list

del region_positions['донецкая народная республика']
del region_positions['запорожская область']
del region_positions['херсонская область']
del region_positions['луганская народная республика']

scale_factor = 1.75
region_positions = {region: [x * scale_factor, y * scale_factor] for region, (x, y) in region_positions.items()}

with open("result_tables/regions_positions.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(["Регион", "Координата X", "Координата Y"])
    for region, (x, y) in region_positions.items():
        writer.writerow([region, x, y])