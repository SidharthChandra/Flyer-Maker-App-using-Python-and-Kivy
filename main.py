import time

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

from utils.flyer_maker import FlyerMaker

Builder.load_file('design.kv')


class MainScreen(Screen):
    PATH = ""

    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self, path):
        if path:
            self.PATH = path[0]
            self.dismiss_popup()

    def show_files(self):
        content = LoadImage(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def download(self, quote, position):
        if quote:
            image_path = self.PATH
            if image_path:
                final_image = FlyerMaker(image_path, quote, position.lower()).execute()
                output_path = image_path.split('.')[0] + '_quote'
                final_image.save(output_path, 'png')
                time.sleep(2)
                self.ids.quote.text = ""
                self.ids.if_no_quote.text = "*Image downloaded"
            else:
                self.ids.if_no_quote.text = "*Please select an image"
        else:
            self.ids.if_no_quote.text = "*Please enter the quote"


class LoadImage(FloatLayout):
    cancel = ObjectProperty(None)
    load = ObjectProperty(None)


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
