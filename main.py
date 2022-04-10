from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import pyttsx3
import vosk_main

red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]


class MainApp(App):
    def build(self):
        layout = BoxLayout(padding=10)
        colors = [red, green, blue, purple]
        button_1 = Button(text='Press to start the companion', background_color=colors[0])
        button_1.bind(on_press=self.on_press_button)
        layout.add_widget(button_1)
        button_2 = Button(text='Guess the song', background_color=colors[2])
        button_2.bind(on_press=self.on_press_button)
        layout.add_widget(button_2)
        return layout

    def on_press_button(self, instance):
        print('You pressed the button!')
        engine = pyttsx3.init()
        engine.say("wait for speak now and say Hello World")
        engine.runAndWait()
        try:
            vosk_main.run(['hello world'])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = MainApp()
    app.run()
