import time
import vk_api
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from VKmethod.VKsearch import VkSearch
import os
import re
import random

class VkAgent(VkSearch):
	"""
	Основной класс взаимодействия пользователя и бота
	"""

	def __init__(self, user_id):
		super().__init__()
		self.user_id = user_id
		self.msg = ''
		self.vk_session = vk_api.VkApi(token=self.token_bot)
		self.user_info = []
		# self.users_id = [7352307, 9681859]  # id администраторов сообщества
		self.users_id = [7352307]  # id администраторов сообщества

	def send_message(self, some_text, buttons=False):
		"""
		Отправка сообщения пользователю.
		Если buttons=True создается клавиатура
		"""
		params = {
			"user_id": self.user_id,
			"message": some_text,
			"random_id": 0}
		if buttons:
			self.get_buttons(params)
		try:
			self.vk_session.method("messages.send", params)
		except requests.exceptions.ConnectionError:
			time.sleep(1)
			self.send_message(some_text)

	def send_message_to_admin(self, user_id):
		text = f"""
		Сообщение от пользователя https://vk.com/id{self.user_id} в чате https://vk.com/gim214214626
		"{self.msg}"
		"""
		params = {
			"user_id": user_id,
			"message": text,
			"random_id": 0}
		try:
			self.vk_session.method("messages.send", params)
		except requests.exceptions.ConnectionError:
			time.sleep(1)
			self.send_message_to_admin(user_id)

	def send_message_to_all_admins(self):
		for user_id in self.users_id:
			self.send_message_to_admin(user_id)

	@staticmethod
	def get_buttons(params: dict):
		keyboard = VkKeyboard(one_time=False, inline=False)
		buttons = ['Записаться', 'Прайс', 'Адрес', 'Наш сайт']
		buttons_color = [
			VkKeyboardColor.PRIMARY,
			VkKeyboardColor.POSITIVE,
			VkKeyboardColor.SECONDARY,
			VkKeyboardColor.POSITIVE
		]
		for btn, btn_color in zip(buttons[:2], buttons_color[:2]):
			keyboard.add_button(btn, btn_color)
		keyboard.add_line()
		for btn, btn_color in zip(buttons[2:], buttons_color[2:]):
			keyboard.add_button(btn, btn_color)
		params['keyboard'] = keyboard.get_keyboard()

	def send_message_buttons(self, some_text):
		pass

	def handler_msg(self):
		"""Функция-обработчик событий сервера типа MESSAGE_NEW"""
		if not self.user_info:
			self.user_info = self.get_info_users()
		self.send_message_to_all_admins()
		if self.verify_hello():
			self.send_hello()  # отправляем приветственное сообщение
		elif self.verify_address():
			self.send_address()  # отправляем адрес
		elif self.verify_entry():
			self.send_link_entry()  # отправляем ссылку на запись
		elif self.verify_price():
			self.send_price()  # отправляем ссылку на прайс
		elif self.verify_contact_admin():
			self.send_contact_admin()  # отправляем данные для связи с руководством
		elif self.verify_thank_you():
			self.send_bay_bay()
		elif self.verify_our_site():
			self.send_site()
		elif self.verify_work_example():
			self.send_work_example()

	def verify_hello(self):
		"""Проверка сообщения на приветствие"""
		pattern = re.compile(r'\b(?:привет|здрав?ств?уй|добрый|доброго\s*времени|рад[а?]\s*видеть)\w*')
		return bool(pattern.findall(self.msg))

	def verify_entry(self):
		"""Проверка сообщения на вхождение запроса о записи на услугу"""
		pattern = re.compile(r'\b(?:запис|окош|окн[ао]|свобод)\w*')
		return bool(pattern.findall(self.msg))

	def verify_price(self):
		"""Проверка сообщения на запрос прайса на услуги"""
		pattern = re.compile(r'\b(?:прайс|цен[аы]|стоит|стоимост|price)\w*')
		return bool(pattern.findall(self.msg))

	def verify_contact_admin(self):
		"""Проверка сообщения на запрос связи с администратором"""
		pattern = re.compile(r'\b(?:админ|руковод|директор|начальств|начальник)\w*')
		return bool(pattern.findall(self.msg))

	def verify_address(self):
		pattern = re.compile(r'\b(?:адрес|вас\s*найти|найти\s*вас|находитесь|добрать?ся|контакты)\w*')
		return bool(pattern.findall(self.msg))

	def verify_work_example(self):
		pattern = re.compile(r'\b(?:примеры?\s*рабо?т|посмотреть\s*рабо?ты|ваших?\s*рабо?ты?|качество\s*рабо?т)\w*')
		return bool(pattern.findall(self.msg))

	def verify_thank_you(self):
		pattern = re.compile(r'\b(?:спасибо|спс|благодар|до\s*свидан|пока)\w*')
		return bool(pattern.findall(self.msg))

	def verify_our_site(self):
		return self.msg == 'наш сайт'

	def send_hello(self):
		text1 = f"Доброго времени суток, {self.user_info['first_name']}! Очень рады видеть вас у нас. Напишите, что бы вы хотели?"
		text2 = f"Здравствуйте, {self.user_info['first_name']}! Очень рады видеть вас у нас. Напишите нам, что вас интересует?"
		text3 = f"Приветствуем Вас, {self.user_info['first_name']}! Рады видеть вас у нас в гостях. Что вас интересует? Напишите пожалуйста"
		text = random.choice([text1, text2, text3])
		self.send_message(some_text=text, buttons=True)

	def send_link_entry(self):
		text = f"""
		{self.user_info['first_name']}, узнать о свободных местах и при желании записаться можно следующими способами:
		- самостоятельно: https://dikidi.net/72910
		- по тел. +7(919)442-35-36
		- через личные сообщения: @id9681859 (Оксана)
		- дождаться сообщения от нашего менеджера
		"""
		self.send_message(some_text=text, buttons=True)

	def send_price(self):
		text = f"""
		{self.user_info['first_name']}, цены на наши услуги можно посмотреть здесь: https://vk.com/uslugi-142029999
		"""
		self.send_message(some_text=text, buttons=True)

	def send_contact_admin(self):
		text = f"""
		{self.user_info['first_name']}, мы обязательно свяжемся с Вами в ближайшее время.
		Кроме того, для связи с руководством Вы можете воспользоваться следующими контактами:
		https://vk.com/id448564047
		https://vk.com/id9681859
		Email: oksarap@mail.ru
		Тел.: +7(919)442-35-36	
		"""
		self.send_message(some_text=text, buttons=True)

	def send_site(self):
		text = f"""
		{self.user_info['first_name']}, много полезной информации о наращивании ресниц смотрите на нашем сайте:
		https://oksa-studio.ru/
		"""
		self.send_message(some_text=text, buttons=True)

	def send_address(self):
		text = """
		Мы находимся по адресу г.Пермь, ул.Тургенева, д.23.
		Это малоэтажное кирпичное здание слева от ТЦ "Агат" 
		Вход через "Идеал-Лик", большой стеклянный тамбур
		https://oksa-studio.ru/contacts/		
		"""
		self.send_message(some_text=text, buttons=True)

	def send_bay_bay(self):
		text1 = f"До свидания, {self.user_info['first_name']}. Будем рады видеть вас снова!"
		text2 = f"До скорых встреч, {self.user_info['first_name']}. Было приятно с Вами пообщаться. Ждём вас снова!"
		text3 = f"Всего хорошего Вам, {self.user_info['first_name']}. Надеюсь мы ответли на Ваши вопросы. Ждём вас снова! До скорых встреч"
		text = random.choice([text1, text2, text3])
		self.send_message(some_text=text, buttons=True)

	def send_work_example(self):
		text = f"""
		{self.user_info['first_name']}, наши работы вы можете посмотреть здесь:
		vk.com/albums-142029999
		"""
		self.send_message(some_text=text, buttons=True)

