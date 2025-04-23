from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from factories.register_classes import register_classes
from ui.gui import LangPulseApp

register_classes()
app = LangPulseApp()
app.run()