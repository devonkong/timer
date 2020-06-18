import kivy
kivy.require('1.11.1')

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

# Window settings
from kivy.core.window import Window
Window.size = (400, 500)
Window.borderless = True

from datetime import datetime, timedelta


class HomeScreen(BoxLayout):
    
    start_time = 0
    end_time = 0
    elapsed_time = 0
    is_timing = False
    
    def timer_button(self, *args):
        """Starts or stops timer when timer button is pressed."""
  
        label = self.ids['timer_button']  # Refers to Label inside Button with id: timer_button
            
        # If not currently timing, start timer
        if not self.is_timing:
            self.start_time = datetime.now()
            self.is_timing = True
            # TODO: Display stopwatch time in real-time
            label.text = 'timer started'  # Update text attribute of Label
        
        # If timer is running, stop timer and record time
        elif self.is_timing:
            self.end_time = datetime.now()
            self.is_timing = False
            self.elapsed_time = self.end_time - self.start_time
            label.text = self.format_time(self.elapsed_time)  # Display formatted elapsed time
           
        
    def format_time(self, timedelta_input):
        """Takes timedelta as input and returns formatted time as string value."""
        
        total_secs = timedelta_input.total_seconds()
        hour = int(total_secs // 3600)
        mins = int((total_secs - 3600 * hour) // 60)
        secs = int((total_secs % 60) // 1)
        
        if hour == 0:
            return f"{mins:02}:{secs:02}"
        elif hour > 0:
            return f"{hour:02}:{mins:02}:{secs:02}"
            
    # TODO: Continue or reset timer

            
class TimerApp(App):
    def build(self):
        return HomeScreen()
    
if __name__ == "__main__":
    TimerApp().run()


