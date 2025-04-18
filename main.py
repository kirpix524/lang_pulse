from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from ui.gui import LangPulseApp

app = LangPulseApp()
app.run()