from kivymd.app import MDApp
from kivy.lang import Builder

# Add this import for exception handling
from kivy.uix.screenmanager import ScreenManager, Screen

class StockPredictionApp(MDApp):
    def build(self):
        try:
            # Load the KV file associated with this app
            Builder.load_file("main.kv")

            # Check if the screen manager is initialized and contains screens
            if not self.root or not isinstance(self.root, ScreenManager) or not self.root.screens:
                print("Error: Screen Manager or screens not properly configured.")
                return None

            # Print the names of all screens in the screen manager
            for screen in self.root.screens:
                print(f"Screen Name: {screen.name}")

            # Set the initial screen (change 'login' to your actual login screen name)
            self.root.current = 'login'

            return self.root
        except Exception as e:
            print(f"Error during build: {e}")
            return None

# Add this if block to ensure the app is run only if this script is the main module
if __name__ == '__main__':
    StockPredictionApp().run()
