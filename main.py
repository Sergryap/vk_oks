import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from VKmethod.VKsearch import VkSearch
from VKmethod.VKagent import VkAgent
import time
import os


def user_bot():
	"""
	Основная функция взаимодействия. Точка входа
	"""
	token = VkSearch.token_bot
	vk_session = vk_api.VkApi(token=token)
	try:
		longpool = VkLongPoll(vk_session)
		users = []
		for event in longpool.listen():
			if event.type == VkEventType.MESSAGE_NEW:
				if event.to_me:
					msg = event.text.lower()
					user_id = event.user_id
					if user_id not in users:
						exec(f"id_{user_id} = VkAgent({user_id})")
						exec(f"id_{user_id}.msg = '{msg}'")
						users.append(user_id)
					else:
						exec(f"id_{user_id}.msg = '{msg}'")
					exec(f"id_{user_id}.handler_msg()")
	except requests.exceptions.ReadTimeout:
		user_bot()


if __name__ == '__main__':
	user_bot()
