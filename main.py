import kivy
kivy.require('1.11.1')

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

# Load kivy file
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
    start_time = 0
    end_time = 0
    elapsed_time = timedelta(seconds=0)
    is_timing = False
    
    def timer_button(self, *args):
        """Starts or stops timer when timer button is pressed."""
        # If not currently timing, start timer
        if not self.is_timing:
            self.start_time = datetime.now()
            self.is_timing = True
            # TODO: Display stopwatch time in real-time
            self.ids['timer_button'].text = 'timer started'  # Update text attribute of Label
            self.ids['reset_button'].opacity = 0  # Hide the reset button
        # If timer is running, stop timer and record time
        elif self.is_timing:
            self.end_time = datetime.now()
            self.is_timing = False
            self.elapsed_time += self.end_time - self.start_time
            self.ids['timer_button'].text = self.format_time(self.elapsed_time)  # Display formatted elapsed time
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
                
                
    def reset_elapsed_time(self):
        """If timer is not running when called, reset elapsed time and hide the reset button."""
        if not self.is_timing:
            self.is_timing = False
            self.elapsed_time = timedelta(seconds=0)
            self.ids['timer_button'].text = '00:00'  # Reset the display
            self.ids['reset_button'].opacity = 0  # Hide the reset button
        else:
            self.timer_button()  # If timer is running, act as an invisible timer button.

    
# Enable navigation between pages
navigator = ScreenManager(transition=NoTransition())
navigator.add_widget(TimerPage(name='timer'))
navigator.add_widget(HomePage(name='home'))  # TODO: Put at top of navigator list

            
class TimerApp(App):
    def build(self):
        return navigator
    
if __name__ == "__main__":
    TimerApp().run()


