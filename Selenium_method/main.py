import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_headers import Headers
import time
import csv
import random
from Selenium_method.authorization import password, tel, url_company, url_service
import pickle
from pprint import pprint
import re


def load_cookies(driver):
	"""Загрузка куков"""
	driver.get(url=url_service)
	# time.sleep(random.uniform(0.5, 1))
	driver.implicitly_wait(5)
	for cookie in pickle.load(open(f"{tel}_cookies", "rb")):
		driver.add_cookie(cookie)


def get_cookies(driver):
	"""Создание куков для url_service"""
	driver.get(url=url_service)
	driver.find_element(by="link text", value="Вход / Регистрация").click()
	time.sleep(random.uniform(0.5, 1))
	driver.find_element(by="link text", value="Мобильный номер").click()
	time.sleep(random.uniform(0.5, 1))
	xpath = '//*[@id="number"]'
	tel_input = driver.find_elements(by="xpath", value=xpath)
	for n in tel:
		tel_input[1].send_keys(n)
		time.sleep(.1)
	time.sleep(random.uniform(0.5, 1))
	password_input = driver.find_element(by="name", value="password")
	for n in password:
		password_input.send_keys(n)
		time.sleep(.1)
	time.sleep(random.uniform(0.5, 1))
	password_input.send_keys(Keys.ENTER)
	time.sleep(random.uniform(0.5, 1))
	pickle.dump(driver.get_cookies(), open(f"{tel}_cookies", "wb"))


def get_click_loader_csv(driver):
	"""Создание клика для загрузки данных из CSV на сайте DIKIDI"""
	load_cookies(driver)
	time.sleep(random.uniform(0.5, 1))
	driver.get(url=url_company)
	time.sleep(random.uniform(3, 8))
	xpath = "/html/body/div[1]/div[2]/div[2]/div[2]/form/div[1]/div[2]/div/button"
	driver.find_element(by="xpath", value=xpath).click()
	time.sleep(random.uniform(0.5, 1))
	xpath = "/html/body/div[1]/div[2]/div[2]/div[2]/form/div[1]/div[2]/div/ul/li[1]/a"
	driver.find_element(by="xpath", value=xpath).click()
	time.sleep(5)


def load_csv_clients():
	"""Загрузка данных из CSV на сайте DIKIDI"""
	driver = get_driver()
	try:
		get_click_loader_csv(driver=driver)
	except Exception as ex:
		print(ex)
	finally:
		driver.close()
		driver.quit()


def get_driver():
	"""Создание драйвера для работы"""
	headers = Headers(os="win", headers=True).generate()
	options = webdriver.ChromeOptions()
	prefs = {"download.default_directory": f"{os.getcwd()}"}
	options.add_experimental_option("prefs", prefs)
	options.add_argument(f"User-Agent={headers['User-Agent']}")
	# options.add_argument("--headless")
	options.headless = True
	options.add_argument("--disable-blink-features=AutomationControlled")
	return webdriver.Chrome(options=options)


def load_info_client(tel_client: str):
	"""Получение данных о времени последней записи клиента по его телефону"""
	driver = get_driver()
	try:
		load_cookies(driver)
		driver.get(url=url_company)
		driver.implicitly_wait(5)
		xpath = "/html/body/div[1]/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[1]/div/input"
		tel_input = driver.find_element(by="xpath", value=xpath)
		tel_input.send_keys(tel_client)
		# for n in tel_client:
		# 	tel_input.send_keys(n)
		# 	time.sleep(.1)
		time.sleep(2)
		verify_data = driver.find_element(by="tag name", value="tbody").find_elements(by="tag name", value="tr")
		if len(verify_data) > 1:
			return None
		lots_data = driver.find_element(by="tag name", value="tbody").find_elements(by="tag name", value="td")
		pattern = re.compile(r"\d{2}\.\d{2}\.\d{4}")
		for data in lots_data:
			if pattern.search(data.text):
				return data.text
	except Exception as ex:
		print(ex)
	finally:
		driver.close()
		driver.quit()


def get_data_client():
	"""Получение данных о клиентах из файла в словарь"""
	with open("clients_2022.08.07.csv", "r", newline='', encoding='utf-8') as csvfile:
		clients = csv.reader(csvfile, delimiter=';')
		return [
					{
						'name': client[0],
						'tel': client[1],
						'amount_vizit': client[9],
						'last_visit': client[10],
						'black_list': client[13]
					} for client in clients][1:]


if __name__ == '__main__':
	# load_csv_clients()
	print(load_info_client(tel_client="2406548"))
# pprint(get_data_client())
