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


class FSMTraining:

	def __init__(self):
		self.data_training = {
			'phone': None,
			'first_name': None,
			'Last_name': None,
		}
		self.data = []

	STEPS = [
		"Хотите больше информации о наших курсах?",
		"Напишите ваш номер телефон",
		"Введите Ваше имя",
		"Введите вашу фамилию",
		"Спасибо, мы обязательно свяжемся с вами",
	]
	TEXT_OFF = "Спасибо, вы можете продолжить в любое время"

	def set_fsm_training(self):
		"""
		Включение/выключение машины состояния опроса записи на обучающий курс
		"""
		pattern_on = re.compile(r'\b(?:обучен|обучить?ся|выучить?ся|научить?ся|курс)\w*')
		pattern_off = re.compile(r'\b(?:отмена|стоп|stop|нет)\w*')
		if bool(pattern_on.findall(self.msg)) and not self.__dict__.get('fsm_training', False):
			self.fsm_training = True
			self.step_count = 1
			self.step_text = FSMIterator(steps=self.STEPS)
			self.iter_training = iter(self.step_text)
		elif bool(pattern_off.findall(self.msg)) and self.__dict__.get('fsm_training', False):
			self.fsm_training = False
			self.send_message(some_text=self.TEXT_OFF, buttons=True)
		elif not self.__dict__.get('fsm_training', False):
			self.fsm_training = False

	def send_msg_fsm_training(self):
		if self.step_count == len(self.STEPS):
			self.fsm_training = False
		self.step_count += 1
		text = next(self.iter_training)
		print(text)
		if self.fsm_training:
			self.send_message(some_text=text, buttons='fsm_training')
			self.data.append(self.msg)
		else:
			self.send_message(some_text=text, buttons=True)
			self.data.append(self.msg)
			for key, value in zip(self.data_training, self.data[2:]):
				self.data_training[key] = value
			print(self.data)
			print(self.data_training)


	def handler_fsm_training(self):
		self.set_fsm_training()
		if self.fsm_training:
			self.send_msg_fsm_training()
			return True
