import json
import random
import time

import pafy
import vlc
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import pyttsx3
import vosk_main

CHALLENGES_FILE = './challenges.json'

red = [1, 0, 0, 1]
green = [0, 1, 0, 1]
blue = [0, 0, 1, 1]
purple = [1, 0, 1, 1]


class MainApp(App):
    def build(self):
        layout = BoxLayout(padding=10)
        colors = [red, green, blue, purple]
        button_1 = Button(text='Trivia', background_color=colors[0])
        button_1.bind(on_press=self.trivia_game)
        layout.add_widget(button_1)
        button_2 = Button(text='Guess the song', background_color=colors[2])
        button_2.bind(on_press=self.music_game)
        layout.add_widget(button_2)
        return layout

    def trivia_game(self, instance):
        with open(CHALLENGES_FILE, 'r') as f:
            challenge_dict = json.load(f)
        random_challenge = challenge_dict[random.randrange(len(challenge_dict))]
        engine = pyttsx3.init()
        engine.setProperty('voice', engine.getProperty('voices')[1].id)
        # engine.say(random_challenge["challenge"])
        # engine.runAndWait()
        try:
            vosk_main.run(random_challenge["challenge"], [random_challenge["answer"]], int(random_challenge["timeout"]))
        except Exception as e:
            print(e)

    def music_game(self, instance):

        url = "https://www.youtube.com/watch?v=rjIiMquPSEo"

        video = pafy.new(url)
        best = video.getbestaudio()

        vlc_instance = vlc.Instance()
        player = vlc_instance.media_player_new()
        media = vlc_instance.media_new(best.url)
        media.add_option('start-time=60')
        media.add_option('run-time=5')
        player.set_media(media)
        player.play()
        time.sleep(5)

if __name__ == '__main__':
    app = MainApp()
    app.run()
