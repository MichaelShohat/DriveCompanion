from kivy.app import App
from kivy.uix.button import Button
import pyttsx3
import vosk_main


class MainApp(App):
    def build(self):
        button = Button(text='Press to start the companion',
                        size_hint=(.5, .5),
                        pos_hint={'center_x': .5, 'center_y': .5})
        button.bind(on_press=self.on_press_button)

        return button

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
