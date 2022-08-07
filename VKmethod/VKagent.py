import time
import vk_api
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from VKmethod.VKsearch import VkSearch
from Data_base.DecorDB import db_insert
import os
import re
import random
from Selenium_method.main import load_info_client


class VkAgent(VkSearch):
	"""
	Основной класс взаимодействия пользователя и бота
	"""

	COMMAND = f"""
	✔️ Помочь записатьcя - "z"
	✔️ Напомнить время последней записи - "r"
	✔️️ Сориентировать по ценам - "p"
	✔️️ Помочь найти нас - "h"
	✔️️ Показать наши работы - "ex"
	✔️️ Связаться с администрацией - "ad"
	✔️️ Начать с начала - "start"
	"""

	def __init__(self, user_id):
		super().__init__()
		self.user_id = user_id
		self.msg = ''
		self.vk_session = vk_api.VkApi(token=self.token_bot)
		self.user_info = []
		self.users_id = [7352307, 448564047, 9681859]  # id администраторов сообщества
		# self.users_id = [7352307]  # id администраторов сообщества

	def send_message(self, some_text, buttons=False, inline=False):
		"""
		Отправка сообщения пользователю.
		Если buttons=True создается клавиатура
		"""
		params = {
			"user_id": self.user_id,
			"message": some_text,
			"random_id": 0}
		if buttons == 'send_photo':
			self.get_button_send_photo(params)
		elif buttons:
			self.get_buttons(params, inline=inline)
		try:
			self.vk_session.method("messages.send", params)
		except requests.exceptions.ConnectionError:
			time.sleep(1)
			self.send_message(some_text)

	def send_message_to_admin(self, user_id):
		text = f"""
		Сообщение от пользователя https://vk.com/id{self.user_id} в чате https://vk.com/gim142029999
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
	def get_buttons(params: dict, inline=False):
		keyboard = VkKeyboard(one_time=False, inline=inline)
		buttons = ['Записаться', 'Start', 'Адрес', 'Примеры работ']
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

	@staticmethod
	def get_button_send_photo(params: dict):
		keyboard = VkKeyboard(one_time=False, inline=True)
		buttons_color = VkKeyboardColor.PRIMARY
		keyboard.add_button('Смoтреть еще', buttons_color)
		params['keyboard'] = keyboard.get_keyboard()

	def send_message_buttons(self, some_text):
		pass

	@db_insert(table='Message')
	def handler_msg(self):
		"""Функция-обработчик событий сервера типа MESSAGE_NEW"""
		if not self.user_info:
			self.user_info = self.get_info_users()
		self.send_message_to_all_admins()
		if self.verify_hello():
			self.send_hello()  # отправляем приветственное сообщение
		if self.verify_address():
			self.send_address()  # отправляем адрес
		elif self.verify_entry():
			self.send_link_entry()  # отправляем ссылку на запись
		elif self.verify_price():
			self.send_price()  # отправляем ссылку на прайс
		elif self.verify_contact_admin():
			self.send_contact_admin()  # отправляем данные для связи с руководством
		elif self.verify_thank_you():
			self.send_bay_bay()  # прощаемся
		elif self.verify_our_site():
			self.send_site()  # отправляем ссылку на сайт
		elif self.verify_work_example():
			self.send_work_example()  # отправляем примеры работ
		elif self.verify_last_service_entry():
			self.send_last_service_entry()  # отправляем время последней записи

	def verify_hello(self):
		"""Проверка сообщения на приветствие"""
		pattern = re.compile(r'\b(?:приве?т|здрав?ств?уй|добрый|доброго\s*времени|рад[а?]\s*видеть|start)\w*')
		return bool(pattern.findall(self.msg))

	def verify_only_hello(self):
		"""Проверка на то, что пользователь отправил только приветствие"""
		verify_all = bool(
			self.verify_entry() or
			self.verify_price() or
			self.verify_contact_admin() or
			self.verify_address() or
			self.verify_our_site()
		)
		return bool(self.verify_hello() and not verify_all)

	def verify_last_service_entry(self):
		b1 = bool(self.msg == "r")
		b2 = bool(self.msg_previous == "r")
		b3 = bool(self.msg not in ["z", "r", "p", "h", "ex", "ad", "start"])
		return b1 or b2 and b3

	def verify_entry(self):
		"""Проверка сообщения на вхождение запроса о записи на услугу"""
		pattern = re.compile(r'\b(?:запис|окош|окн[ао]|свобод|хочу\s*нар[ао]стить)\w*')
		return bool(pattern.findall(self.msg) or self.msg == 'z')

	def verify_price(self):
		"""Проверка сообщения на запрос прайса на услуги"""
		pattern = re.compile(r'\b(?:прайс|цен[аы]|стоит|стоимост|price)\w*')
		return bool(pattern.findall(self.msg) or self.msg == 'p' or self.msg == 'р')

	def verify_contact_admin(self):
		"""Проверка сообщения на запрос связи с администратором"""
		pattern = re.compile(r'\b(?:админ|руковод|директор|начальств|начальник)\w*')
		return bool(pattern.findall(self.msg) or self.msg == 'ad')

	def verify_address(self):
		pattern = re.compile(r'\b(?:адрес|вас\s*найти|найти\s*вас|находитесь|добрать?ся|контакты|где\s*ваш\s*офис)\w*')
		return bool(pattern.findall(self.msg) or self.msg == 'h')

	def verify_work_example(self):
		pattern = re.compile(r'\b(?:примеры?\s*рабо?т|посмотреть\s*рабо?ты|ваших?\s*рабо?ты?|качество\s*рабо?т|наши работы|смoтреть еще)\w*')
		return bool(pattern.findall(self.msg) or self.msg == 'ex')

	def verify_thank_you(self):
		pattern = re.compile(r'\b(?:спасибо|спс|благодар|до\s*свидан|пока)\w*')
		return bool(pattern.findall(self.msg))

	def verify_our_site(self):
		return bool(self.msg == 'наш сайт' or self.msg == 'site')

	def send_hello(self, inline=False):
		d = [
			'\nНапишите, что бы вы хотели или выберите ниже.',
			'\nНапишите мне, что вас интересует или выберите ниже.',
			'\nЧто вас интересует? Напишите пожалуйста или выберите ниже.'
		]

		t = f"""
		Пока менеджеры заняты я могу:
		{self.COMMAND}
		"""

		delta = random.choice(d) if self.verify_only_hello() else ''
		t1 = f"Доброго времени суток, {self.user_info['first_name']}!\nЯ бот Oksa-studio.\nБуду рад нашему общению.\n{t}{delta}"
		t2 = f"Здравствуйте, {self.user_info['first_name']}!\nЯ чат-бот Oksa-studio.\nОчень рад видеть Вас у нас.\n{t}{delta}"
		t3 = f"Приветствуем Вас, {self.user_info['first_name']}!\nЯ бот этого чата.\nРад видеть Вас у нас в гостях.\n{t}{delta}"
		text = random.choice([t1, t2, t3])
		self.send_message(some_text=text, buttons=True, inline=inline)

	def send_link_entry(self):
		text = f"""
		{self.user_info['first_name']}, узнать о свободных местах, своих записях и/или записаться можно:\n
		✔️ Самостоятельно: https://dikidi.net/72910
		✔️ По тел. +7(919)442-35-36
		✔️ Через личные сообщения: @id9681859 (Оксана)
		✔ Дождаться сообщения от нашего менеджера\n
		Что вас еще интересует напишите или выберите ниже.
		"""
		self.send_message(some_text=text, buttons=True)

	def send_last_service_entry(self):
		if self.msg == "r":
			text_request = f"""
			{self.user_info['first_name']},
			напишите Ваш номер телефона, по которому вы записывались, чтобы найти вашу запись.
			
			Либо введите другую команду:
			{self.COMMAND}
			"""
			self.send_message(some_text=text_request, buttons=True)
		if self.msg_previous == "r" and self.msg != "r":
			self.send_message(some_text="Немного подождите. Получаю данные...", buttons=True)
			answer = load_info_client(tel_client=self.msg)
			if answer:
				text_answer = f"""
				{self.user_info['first_name']},
				Дата и время вашей последней записи:
				✔{answer} 
				
				Выберите команду:
				{self.COMMAND}
				"""
			else:
				text_answer = f"""
				{self.user_info['first_name']},
				Извините, но я не нашел у вас ни одной записи.
				Возможно вам нужно уточнить номер телефона.
				
				Для продолжения выберите команду:				
				{self.COMMAND}
				"""
			self.send_message(some_text=text_answer, buttons=True)

	def send_price(self):
		text = f"""
		{self.user_info['first_name']}, цены на наши услуги можно посмотреть здесь:
		✔️https://vk.com/uslugi-142029999\n
		Что вас еще интересует напишите или выберите ниже.
		"""
		self.send_message(some_text=text, buttons=True)

	def send_contact_admin(self):
		text = f"""
		{self.user_info['first_name']}, мы обязательно свяжемся с Вами в ближайшее время.
		Кроме того, для связи с руководством Вы можете воспользоваться следующими контактами:
		✔ https://vk.com/id448564047
		✔ https://vk.com/id9681859
		✔ Email: oksarap@mail.ru
		✔ Тел.: +7(919)442-35-36	
		"""
		self.send_message(some_text=text, buttons=True)

	def send_site(self):
		text = f"""
		{self.user_info['first_name']}, много полезной информации о наращивании ресниц смотрите на нашем сайте:
		https://oksa-studio.ru/
		\nЧто вас еще интересует напишите или выберите ниже.
		"""
		self.send_message(some_text=text, buttons=True)

	def send_address(self):
		text1 = f"""
		{self.user_info['first_name']}, мы находимся по адресу:\n
		📍 г.Пермь, ул.Тургенева, д.23.\n
		"""
		text2 = """
		Это малоэтажное кирпичное здание слева от ТЦ "Агат" 
		Вход через "Идеал-Лик", большой стеклянный тамбур\n
		Что вас еще интересует напишите или выберите ниже.	
		"""
		self.send_message(some_text=text1, buttons=True)
		self.send_photo('photo-195118308_457239030')
		self.send_message(some_text=text2, buttons=False)

	def send_bay_bay(self):
		text1 = f"До свидания, {self.user_info['first_name']}. Будем рады видеть вас снова!"
		text2 = f"До скорых встреч, {self.user_info['first_name']}. Было приятно с Вами пообщаться. Ждём вас снова!"
		text3 = f"Всего доброго Вам, {self.user_info['first_name']}. Надеюсь мы ответили на Ваши вопросы. Ждём вас снова! До скорых встреч."
		text = random.choice([text1, text2, text3])
		self.send_message(some_text=text, buttons=True)

	def send_work_example(self):
		text = f"""
		{self.user_info['first_name']}, больше работ здесь:
		vk.com/albums-142029999
		Что вас еще интересует напишите или выберите ниже.
		"""
		self.send_photo()
		self.send_message(some_text=text, buttons='send_photo')

	def send_photo(self, photo_id=None):
		attachment = photo_id if photo_id else self.get_photos_example()
		self.vk_session.method("messages.send", {
			"user_id": self.user_id,
			"attachment": attachment,
			"random_id": 0})
