from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class TimerBar(Widget):
    progress = NumericProperty(1.0)  # от 1.0 до 0.0

    __events__ = ("on_complete",)  # 👈 регистрация пользовательского события

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._event = None
        self._remaining = None
        self._interval = None
        with self.canvas.before:
            self.color = Color(0, 1, 0, 1)  # зелёный
            self.rect = RoundedRectangle (pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect, progress=self._update_rect)

    def _update_rect(self, *args):
        full_width = self.width
        self.rect.pos = self.pos
        self.rect.size = (full_width * self.progress, self.height)
        # Обновим цвет: от зелёного к жёлтому, затем к красному
        if self.progress > 0.5:
            # от зелёного (0,1,0) к жёлтому (1,1,0)
            r = 2 * (1 - self.progress)
            self.color.rgba = (r, 1, 0, 1)
        else:
            # от жёлтого (1,1,0) к красному (1,0,0)
            g = 2 * self.progress
            self.color.rgba = (1, g, 0, 1)

    def start(self, interval: float):
        self.progress = 1.0
        self._interval = interval
        self._remaining = interval
        self._event = Clock.schedule_interval(self._tick, 0.05)

    def stop(self):
        if hasattr(self, '_event') and self._event:
            self._event.cancel()

    def _tick(self, dt):
        self._remaining -= dt
        self.progress = max(0, self._remaining / self._interval)
        if self._remaining <= 0:
            self._event.cancel()
            self.dispatch("on_complete")

    def on_complete(self):
        pass  # перехватывается в родителе, если нужно

    def cancel(self):
        if hasattr(self, '_event') and self._event:
            self._event.cancel()
