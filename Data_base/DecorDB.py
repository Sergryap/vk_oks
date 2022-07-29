import time
from datetime import date
from functools import wraps
from sqlalchemy.exc import OperationalError
from Data_base.create_schema import Client, Entry, Service, Message
from Data_base.methodsDB import DbMethods
from datetime import datetime


class DBConnect(DbMethods):

	def data_base_insert(self, table: str, data: dict):
		"""Вставка данных в таблицы базы данных"""
		try:
			if table == 'Client':
				self.insert_client(data)
			if table == 'Message':
				self.insert_msg()
		except OperationalError:
			self.data_base_insert(table, data)

	def insert_client(self, data: dict):
		"""Вставка одной строки в таблицу Client"""
		if self.verify_insert_client():
			data['bdate'] = self.date_format(data['bdate'])
			if not data['bdate']:
				del data['bdate']
			if not data['city_id']:
				del data['city_id']
			session = self.Session()
			user_add = Client(**data)
			session.add(user_add)
			session.commit()

	def insert_msg(self):
		data = {
			'user_id': self.user_id,
			'time_message': datetime.now(),
			'message': self.msg
		}
		session = self.Session()
		user_add = Message(**data)
		session.add(user_add)
		session.commit()

	def verify_insert_client(self):
		"""Проверка вхождения пользователя в таблицу User"""
		sel = self.conn.execute(f"""
			SELECT user_id
			FROM client
			WHERE user_id = {self.user_id}
			""").fetchall()
		return not sel

	@staticmethod
	def date_format(birth_date: str):
		"""Запись даты в формате fromisoformat"""
		if birth_date:
			if len(birth_date.split(".")) == 3:
				date_info = time.strptime(birth_date, "%d.%m.%Y")
				year = date_info.tm_year
				month = date_info.tm_mon
				day = date_info.tm_mday
				month = month if month > 9 else str(f"0{month}")
				day = day if day > 9 else str(f"0{day}")
				return date.fromisoformat(f'{year}-{month}-{day}')


def db_insert(table: str):
	"""Декоратор для вставки данных в таблицу table"""

	def dbase(old_func):
		@wraps(old_func)
		def new_func(self, *args, **kwargs):
			result = old_func(self, *args, **kwargs)
			self.data_base_insert(table=table, data=result)
			return result

		return new_func

	return dbase
