import kivy
kivy.require('1.11.1')

from kivy.app import App

# Kivy UI elements
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from kivy.clock import Clock

# Load Kivy file
from kivy.lang import Builder
Builder.load_file("layout.kv")

# Window settings
from kivy.core.window import Window
Window.size = (400, 500)
Window.borderless = True

from datetime import datetime, timedelta


class HomePage(Screen):
    pass
    

class TimerPage(Screen):
    elapsed_time = timedelta(seconds=0)
    is_timing = False
    display_secs = 0
    
    def start_stop(self, *args):
        """Starts or stops timer when timer button is pressed."""
        # If not currently timing, start timer
        if not self.is_timing:
            self.is_timing = True
            self.start_time = datetime.now() 
            Clock.schedule_interval(self.update_time, 0)  # Continuously update timer display
            self.ids['reset_button'].opacity = 0  # Hide the reset button
        # If timer is running, stop timer and record time
        elif self.is_timing:
            self.is_timing = False
            Clock.unschedule(self.update_time)
            self.end_time = datetime.now()
            self.elapsed_time += self.end_time - self.start_time
            self.ids['start_stop_button'].text = self.format_time(self.elapsed_time)  # Display formatted elapsed time
            self.ids['reset_button'].opacity = 1  # Show the reset button
    
    def format_time(self, timedelta_input):
            """Takes timedelta as input and returns formatted time as string value."""
            total_secs = timedelta_input.total_seconds()
            hour = int(total_secs // 3600)
            mins = int((total_secs - 3600 * hour) // 60)
            secs = int((total_secs % 60) // 1)
            # Return MM:SS if under an hour, else return HH:MM:SS
            if hour == 0:
                return f"{mins:02}:{secs:02}"
            elif hour > 0:
                return f"{hour:02}:{mins:02}:{secs:02}"
   
    def update_time(self, nap):
        """Update timer display."""
        self.display_secs += nap
        self.ids['start_stop_button'].text = self.format_time(timedelta(seconds=self.display_secs))
                              
    def reset_elapsed_time(self):
        """If timer is not running and has not already been reset when called, reset elapsed time and hide the reset button."""
        if not self.is_timing and self.elapsed_time != timedelta(seconds=0):
            self.is_timing = False
            self.elapsed_time = timedelta(seconds=0)
            self.display_secs = 0
            self.ids['start_stop_button'].text = '00:00'  # Reset the display
            self.ids['reset_button'].opacity = 0  # Hide the reset button
        else:
            self.start_stop()  # If timer is running, act as an invisible timer button.

    
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


