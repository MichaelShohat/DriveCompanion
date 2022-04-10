from kivy.app import App
from kivy.uix.button import Button
import pyttsx3
import speech_recognition as sr


class MainApp(App):
    def build(self):
        button = Button(text='Press to start the companion',
                        size_hint=(.5, .5),
                        pos_hint={'center_x': .5, 'center_y': .5})
        button.bind(on_press=self.on_press_button)

        return button

    def on_press_button(self, instance):
        print('You pressed the button!')
        r = sr.Recognizer()
        engine = pyttsx3.init()
        engine.say("wait for speak now and say Hello World")
        engine.runAndWait()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            engine.say("Speak now")
            engine.runAndWait()
            try:
                audio = r.listen(source, timeout=3.0)
            except sr.WaitTimeoutError as e:
                engine.say("You didn't say anything")
                engine.runAndWait()
        try:
            print("Sphinx thinks you said " + r.recognize_sphinx(audio, keyword_entries=[("hello", 0.9), ("world", 0.9)]))
        except sr.UnknownValueError:
            engine.say("You didn't say anything I can understand")
            engine.runAndWait()
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
        except UnboundLocalError as e:
            pass



if __name__ == '__main__':
    app = MainApp()
    app.run()
