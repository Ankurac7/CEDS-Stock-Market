import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('design.kv')

class MyGridLayout(Widget):
    name=ObjectProperty(None)
    email=ObjectProperty(None)
    phno=ObjectProperty(None)
    
    def press(self):
        name=self.name.text
        email=self.email.text
        phno=self.phno.text

        print(f'Hello {name}, your mail is {email}, and your number is {phno}')
        # Print it to the screen
        #self.add_widget(Label(text=f'Hello {name}, your mail is {email}, and your number is {phno}'))

        # Clear the input boxes
        self.name.text=""
        self.email.text=""
        self.phno.text=""

class ElderApp(App):
    def build(self):
        return MyGridLayout()
    
if __name__== '__main__':
    ElderApp().run()