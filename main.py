import kivy
from kivy.app import App
kivy.require('1.11.1')

# Kivy UI modules
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

# Time tracking modules
from kivy.clock import Clock
from datetime import datetime, timedelta

# Load Kivy file
from kivy.lang import Builder
Builder.load_file("style.kv")

# Set colour palette
import kivy.utils as utils
bg_col = utils.get_color_from_hex('#1E1E1E')
text_col_main = utils.get_color_from_hex('#DDDDDD')
text_col_secondary = utils.get_color_from_hex('#555555')

# App settings
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', 'True')
Config.set('graphics', 'resizable', 'False')

# Window settings
from kivy.core.window import Window
Window.size = (400, 500)
Window.top = 0
Window.left = 0
Window.borderless = False
Window.fullscreen = False
Window.clearcolor = bg_col


class HomePage(Screen):
    pass


class TimerPage(Screen):
    elapsed_time = timedelta(seconds=0)
    is_timing = False

    def start_stop(self, *args):
        """Starts or stops timer when timer button is pressed."""
        # If not currently timing, start timer
        if not self.is_timing:
            self.is_timing = True
            self.start_time = datetime.now()
            self.ids['start_stop_button'].color = text_col_main
            Clock.schedule_interval(self.update_time, 0)  # Continuously update timer display
            self.ids['reset_button'].opacity = 0  # Hide the reset button
        # If timer is running, stop timer and record time
        elif self.is_timing:
            self.is_timing = False
            Clock.unschedule(self.update_time)
            self.end_time = datetime.now()
            self.elapsed_time += self.end_time - self.start_time
            self.ids['start_stop_button'].color = text_col_secondary
            self.ids['start_stop_button'].text = self.format_time(
                self.elapsed_time)  # Display formatted elapsed time
            self.ids['reset_button'].opacity = 1  # Show the reset button

    def format_time(self, timedelta_input):
        """Takes timedelta as input and returns formatted time as string value."""
        total_secs = timedelta_input.total_seconds()
        hours = int(total_secs // 3600)
        mins = int((total_secs - 3600 * hours) // 60)
        secs = int((total_secs % 60) // 1)
        # Return MM:SS if under an hours, else return HH:MM:SS
        if hours == 0:
            return f"{mins:02}:{secs:02}"
        elif hours > 0:
            return f"{hours}:{mins:02}:{secs:02}"

    def update_time(self, *args):
        """Update timer display."""
        self.ids['start_stop_button'].text = self.format_time(
            datetime.now() - self.start_time + self.elapsed_time)

    def reset_elapsed_time(self):
        """If timer is not running and has not already been reset when called, reset elapsed time and hide the reset button."""
        if not self.is_timing and self.elapsed_time != timedelta(seconds=0):
            self.is_timing = False
            self.elapsed_time = timedelta(seconds=0)
            self.ids['start_stop_button'].color = text_col_secondary
            self.ids['start_stop_button'].text = '00:00'  # Reset the display
            self.ids['reset_button'].opacity = 0  # Hide the reset button
        else:
            self.start_stop()  # If timer is running, act as an invisible timer button


# Enable navigation between pages
navigator = ScreenManager(transition=NoTransition())
navigator.add_widget(TimerPage(name='timer'))
navigator.add_widget(HomePage(name='home'))  # TODO: Put at top of navigator list


# Core app
class TimerApp(App):
    def build(self):
        return navigator


# App launcher
if __name__ == "__main__":
    TimerApp().run()
