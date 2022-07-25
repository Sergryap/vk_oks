import time
from Vkmethod.VkSearch import VkSearch
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
		pass

	def msg_entry(self):
		"""Проверка сообщения на вхождение запроса о записи на услугу"""
		pass

	def msg_price(self):
		"""Проверка сообщения на запрос прайса на услуги"""
		pass

	def msg_info(self):
		"""Проверка сообщения на вхождение запроса об общей информации"""
		pass

	def msg_contact_admin(self):
		"""Проверка сообщения на запрос связи с администратором"""

