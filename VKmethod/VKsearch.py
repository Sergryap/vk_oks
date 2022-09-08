import requests
import json
import os
import datetime as dt
import time
import random

from Data_base.DecorDB import db_insert
from Data_base.DecorDB import DBConnect
from FSMstate import FSMQuiz
from pprint import pprint
from VKmethod.photos import photos


class VkSearch(FSMQuiz, DBConnect):
    """Класс методов поиска и сортировки из api-vk"""

    url = 'https://api.vk.com/method/'
    with open(os.path.join("VKmethod", "token.txt"), encoding='utf-8') as file:
        token = [t.strip() for t in file.readlines()]
    # with open(os.path.join("token.txt"), encoding='utf-8') as file:
    #     token = [t.strip() for t in file.readlines()]
    token_bot = token[0]
    token = token[1:]

    def __init__(self):
        super().__init__()
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

    @db_insert(table="Client")
    def get_info_users(self):
        """
        Получение данных о пользователе по его id
        :return: словарь с данными по пользователю
        """
        params_delta = {'user_ids': self.user_id, 'fields': 'country,city,bdate,sex'}
        response = self.get_stability('users.get', params_delta)
        if response:
            birth_date = self.get_birth_date(response)
            return {
                'user_id': self.user_id,
                'city_id': None if not response['response'][0].get('city') else response['response'][0]['city'].get('id'),
                'sex': response['response'][0]['sex'],
                'first_name': response['response'][0]['first_name'],
                'last_name': response['response'][0]['last_name'],
                'bdate': birth_date,
            }

    @staticmethod
    def get_birth_date(res: dict):
        """
        Получение данных о возрасте пользователя
        :return: кортеж с датой: str и годом рождения: int
        """
        birth_date = None if 'bdate' not in res['response'][0] else res['response'][0]['bdate']
        if birth_date:
            birth_date = None if len(birth_date.split('.')) < 3 else birth_date
        return birth_date

    def __albums_id(self, owner_id):
        """
        Cоздает список, содержащий id альбомов пользователя
        """
        params_delta = {'owner_id': owner_id, 'need_system': ''}
        response = self.get_stability('photos.getAlbums', params_delta)
        if response and response['response']['items']:
            albums_id = []
            for item in response['response']['items']:
                albums_id.append(item['id'])
            return albums_id

    def __photos_get(self, owner_id, album_id):
        """
        Получение данных по фотографиям из одного альбома (album_id) пользователя (owner_id)
        :return: список содержащий id photo
        """
        params_delta = {'owner_id': owner_id, 'album_id': album_id, 'extended': 1}
        response = self.get_stability('photos.get', params_delta)
        if response:
            photos_info = []
            for item in response['response']['items']:
                photos_info.append(f"photo{owner_id}_{item['id']}")
            return photos_info

    def get_photos_total(self):
        albums = self.__albums_id('-142029999')
        all_photos = []
        for album in albums:
            all_photos += self.__photos_get('-142029999', album)
        return all_photos

    @staticmethod
    def get_photos_example():
        attachment = ''
        for photo in random.sample(photos, 5):
            attachment += f"{photo},"
        return attachment[:-1]
