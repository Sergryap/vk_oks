from vk_api.keyboard import VkKeyboard, VkKeyboardColor

class MyKeyButton:

	@staticmethod
	def get_buttons(params: dict):
		keyboard = VkKeyboard(one_time=False, inline=False)
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

	@staticmethod
	def get_button_fsm_quiz(params: dict):
		keyboard = VkKeyboard(one_time=False, inline=False)
		buttons = ['Отмена', 'Пропустить']
		btn_color = VkKeyboardColor.PRIMARY
		for btn in buttons:
			keyboard.add_button(btn, btn_color)
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	def get_button_training(params: dict):
		keyboard = VkKeyboard(one_time=False, inline=True)
		buttons_color = VkKeyboardColor.PRIMARY
		keyboard.add_button('Заполнить анкету', buttons_color)
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	def get_button_break(params: dict):
		keyboard = VkKeyboard(one_time=False, inline=True)
		buttons_color = VkKeyboardColor.PRIMARY
		keyboard.add_button('Отменить', buttons_color)
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	def get_practic_extention(params: dict):
		keyboard = VkKeyboard(one_time=False, inline=True)
		buttons = ['Да', 'Нет']
		btn_color = VkKeyboardColor.PRIMARY
		for btn in buttons:
			keyboard.add_button(btn, btn_color)
		params['keyboard'] = keyboard.get_keyboard()


	@staticmethod
	def get_what_job(params: dict):
		keyboard = VkKeyboard(one_time=False, inline=True)
		buttons = ['Пропустить', 'Пропустить', 'Пропустить', 'Пропустить', 'Конец']
		btn_color = VkKeyboardColor.SECONDARY
		for i, btn in enumerate(buttons, start=1):
			keyboard.add_button(btn, btn_color)
			if i != len(buttons):
				keyboard.add_line()
		params['keyboard'] = keyboard.get_keyboard()
