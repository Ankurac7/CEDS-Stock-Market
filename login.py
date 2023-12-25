from kivy.lang import Builder
from kivymd.app import MDApp


class StockPredictionApp(MDApp):

	data = {
    "Register": "account-plus",
    "Exit": "close"
	}

	def callback(self, instance):
		if instance.icon == 'account-plus':
			lang = "Register"
		elif instance.icon == 'close':
			lang = "Exit"

		self.root.ids.my_label.text = f'You Pressed {lang}'


	def build(self):
		self.theme_cls.theme_style= "Light"
		self.theme_cls.primary_palette = "DeepPurple"
		return Builder.load_file('login.kv')
	def logger(self):
		self.root.ids.login_page.text= f'Sup {self.root.ids.user.text}!'
	def clear(self):
		self.root.ids.login_page.text= "Login Page"
		self.root.ids.user.text= ""
		self.root.ids.password.text= ""


StockPredictionApp().run()