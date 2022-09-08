import re


class FSMIterator:

	def __init__(self, steps: list):
		self.steps = steps

	def __iter__(self):
		self.ind = 0
		return self

	def __next__(self):
		if self.ind == len(self.steps):
			raise StopIteration
		value = self.steps[self.ind]
		self.ind += 1
		return value


class FSMQuiz:
	"""
	Класс квиза записи на курс
	"""

	def __init__(self):
		self.data_quiz = {
			'phone': None,
			'first_name': None,
			'Last_name': None,
			'practice': None,
			'work': None,
		}
		self.data_quiz_list = []

	TEXT_OFF = 'Спасибо, вы можете продолжить в любое время. Просто отправьте "обучение" или "ed".'

	def verify_phone(self):
		pattern = re.compile(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$')
		return bool(pattern.findall(self.msg))


	def get_steps_quiz(self):
		return [
			f"1. {self.user_info['first_name']}, оставьте пожалуйста ваш контактный номер телефона:",
			"2. Введите ваше имя",
			"3. Введите вашу фамилию",
			"4. Вы уже имеете опыт в наращивании ресниц?",
			"5. Кем вы сейчас работаете или чем занимаетесь?",
			"Спасибо, мы обязательно свяжемся с вами и сообщим всю необходимую информацию.",
		]

	def set_fsm_quiz(self):
		"""
		Включение/выключение машины состояния опроса записи на обучающий курс
		"""
		# pattern_on = re.compile(r'\b(?:обучен|обучить?ся|выучить?ся|научить?ся|курс)\w*')
		pattern_on = re.compile(r'\b(?:анкета|заполнить анкету)\w*')
		pattern_off = re.compile(r'\b(?:отмена|отменить|стоп|stop)\w*')

		if bool(pattern_on.findall(self.msg)) and not self.__dict__.get('fsm_quiz', False):
			self.fsm_quiz = True
			self.step_count = 1
			self.step_text = FSMIterator(steps=self.get_steps_quiz())
			self.iter_quiz = iter(self.step_text)
		elif bool(pattern_off.findall(self.msg)) and self.__dict__.get('fsm_quiz', False):
			self.fsm_quiz = False
			self.data_quiz_list = []
			self.send_message(some_text=self.TEXT_OFF, buttons=True)
		elif not self.__dict__.get('fsm_quiz', False):
			self.fsm_quiz = False

	def send_msg_fsm_quiz(self):
		"""
		Пошаговая отправка сообщений опроса
		"""
		if self.step_count == len(self.get_steps_quiz()):
			self.fsm_quiz = False
		if self.step_count == 2 and not self.verify_phone():
			text = "Укажите номер телефона в верном формате, например: 7(999)999-99-99. Либо отмените заполнение анкеты"
			buttons = 'break'
		elif self.step_count == 4:
			text = next(self.iter_quiz)
			buttons = 'practic_extention'
			self.step_count += 1
		elif self.step_count == 5:
			text = next(self.iter_quiz)
			buttons = 'what_job'
			self.step_count += 1
		else:
			text = next(self.iter_quiz)
			buttons = 'fsm_quiz'
			self.step_count += 1

		print(text)
		if self.fsm_quiz:
			self.send_message(some_text=text, buttons=buttons)
			self.data_quiz_list.append(self.msg)
		else:
			self.send_message(some_text=text, buttons=True)
			self.data_quiz_list.append(self.msg)
			for key, value in zip(self.data_quiz, self.data_quiz_list[1:]):
				self.data_quiz[key] = value
			self.data_quiz_list = []
			print(self.data_quiz_list)
			print(self.data_quiz)

	def handler_fsm_quiz(self):
		self.set_fsm_quiz()
		if self.fsm_quiz:
			self.send_msg_fsm_quiz()
			return True
