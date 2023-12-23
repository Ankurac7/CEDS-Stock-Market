import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class MyGridLayout(GridLayout):
    # Initialize infinite keywords
    def __init__(self, **kwargs):
        # Call grid layout constructor
        super(MyGridLayout,self).__init__(**kwargs)
        # Set columns
        self.cols=1
        self.row_force_default=True
        self.row_default_height=120
        self.col_force_default=True
        self.col_default_width=100
        # Create a second grid layout
        self.top_grid=GridLayout(
            row_force_default=True,
            row_default_height=40,
            col_force_default=True,
            col_default_width=100
        )
        self.top_grid.cols=2



        # Add widgets
        self.top_grid.add_widget(Label(text="Name: "))
        # Add Input Box
        self.name= TextInput(multiline=False)
        self.top_grid.add_widget(self.name)

        self.top_grid.add_widget(Label(text="Email: "))
        self.email= TextInput(multiline=False)
        self.top_grid.add_widget(self.email)

        self.top_grid.add_widget(Label(text="Phone Number: "))
        self.phno= TextInput(multiline=False)
        self.top_grid.add_widget(self.phno)
        # Add the new top grid to our App
        self.add_widget(self.top_grid)

        # Create a submit button
        self.submit= Button(text="Submit", 
                            font_size=32,
                            size_hint_y= None,
                            height=50,
                            size_hint_x= None,
                            width=200)
        self.submit.bind(on_press=self.press)
        self.add_widget(self.submit)

    def press(self,instance):
        name=self.name.text
        email=self.email.text
        phno=self.phno.text

        #print(f'Hello {name}, your mail is {email}, and your number is {phno}')
        # Print it to the screen
        self.add_widget(Label(text=f'Hello {name}, your mail is {email}, and your number is {phno}'))

        # Clear the input boxes
        self.name.text=""
        self.email.text=""
        self.phno.text=""

class MyApp(App):
    def build(self):
        return MyGridLayout()
    
if __name__== '__main__':
    MyApp().run()