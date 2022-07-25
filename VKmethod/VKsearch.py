import requests
import json
import os
import datetime as dt
import time


class VkSearch:
    """Класс методов поиска и сортировки из api-vk"""

    url = 'https://api.vk.com/method/'
    with open(os.path.join("VKmethod", "token.txt"), encoding='utf-8') as file:
        token = [t.strip() for t in file.readlines()]
    token_bot = token[0]
    token = token[1:]

    def __init__(self):
        # super().__init__()
        self.params = {'access_token': self.token[0], 'v': '5.131'}
        self.author = 0

    def __set_params(self, zero=True):
        """Установка параметров для get запроса при неудачном запросе"""
        self.author = 0 if zero else self.author + 1
        print(f'Токен заменен на >>> {self.author}!')
        self.params = {'access_token': self.token[self.author], 'v': '5.131'}

    def get_stability(self, method, params_delta, i=0):
        """
        Метод get запроса с защитой на случай блокировки токена
        При неудачном запросе делается рекурсивный вызов
        с другим токеном и установкой этого токена по умолчанию
        через функцию __set_params
        Для работы функции необходим текстовый файл token.txt с построчно записанными токенами
        В первую строку заносится токен от чат-бота.
        """
        print(f'Глубина рекурсии: {i}/токен: {self.author}')
        method_url = self.url + method
        response = requests.get(method_url, params={**self.params, **params_delta}).json()
        if 'response' in response:
            return response
        elif i == len(self.token) - 1:
            return False
        elif self.author < len(self.token) - 1:
            self.__set_params(zero=False)
        elif self.author == len(self.token) - 1:
            self.__set_params()
        count = i + 1  # счетчик стэков вызова
        return self.get_stability(method, params_delta, i=count)
