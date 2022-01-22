from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from datetime import datetime
from pathlib import Path
import json
import glob
import random

Builder.load_file('design.kv')


class LoginScreen(Screen):
    def login(self, username, password):
        with open('users.json') as file:
            users = json.load(file)
        if username in users and users[username]['password'] == password:
            self.manager.transition.direction = 'left'
            self.manager.current = 'login_screen_success'
        else:
            self.ids.login_wrong.text = "Wrong username or password!"

    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def forgot_pw(self):
        self.manager.current = "forgot_password_screen"


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings]
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try a different feeling!"


class ForgotPasswordScreen(Screen):
    def play_video(self):
        self.ids.video.state = "play"


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class SignUpScreen(Screen):
    def add_user(self, username, password):
        with open('users.json') as file:
            users = json.load(file)

        if username not in users:
            users[username] = {'username': username,
                               'password': password,
                               'created': datetime.now().strftime('%Y-%m-%d %H-%M-%S')}
            with open('users.json', 'w') as file:
                json.dump(users, file)
            self.manager.current = 'sign_up_screen_success'

        else:
            self.ids.user_exists.text = "User already exists!"


class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
