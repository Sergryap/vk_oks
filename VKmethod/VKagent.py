import time
import vk_api
from VKmethod.VKsearch import VkSearch
import os
import re


class VkAgent(VkSearch):
	"""
	Основной класс взаимодействия пользователя и бота
	"""
	def __init__(self, user_id):
		super().__init__()
		self.user_id = user_id
		self.msg = ''
		self.vk_session = vk_api.VkApi(token=self.token_bot)
		self.waiting_message = False

	def handler_msg(self):
		"""Функция-обработчик событий сервера типа MESSAGE_NEW"""
		if self.msg_entry():
			return self.send_link_entry()  # отправляем ссылку на запись
		elif self.msg_price():
			return self.send_price()  # отправляем ссылку на прайс
		elif self.msg_contact_admin():
			return self.send_contact_admin()  # отправляем данные для связи с руководством
		else:
			return self.send_info_eyas()  # отправляем ссылку на общую информацию

	def msg_entry(self):
		"""Проверка сообщения на вхождение запроса о записи на услугу"""
		pattern = re.compile(r'\b(?:запис|окош|окн[ао]|свобод)\w*')
		return bool(pattern.findall(self.msg))

	def msg_price(self):
		"""Проверка сообщения на запрос прайса на услуги"""
		pattern = re.compile(r'\b(?:прайс|цен[аы]|стоит|стоимост|price)\w*')
		return bool(pattern.findall(self.msg))

	def msg_contact_admin(self):
		"""Проверка сообщения на запрос связи с администратором"""
		pattern = re.compile(r'\b(?:админ|руковод|директор|)\w*')
		return bool(pattern.findall(self.msg))

	def msg_info(self):
		"""Проверка сообщения на вхождение запроса об общей информации"""
		pass


if __name__ == '__main__':
	test = VkAgent(7575757)
