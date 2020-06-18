import kivy
kivy.require('1.11.1')

from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

import time


class HomeScreen(BoxLayout):
    
    start_time = 0
    end_time = 0
    elapsed_time = 0
    is_timing = False
    
    def timer_button(self, *args):
        # Runs when the timer button is pressed
        
        label = self.ids['timer_button']  # Refers to Label inside Button with id: timer_button
        
        # If not currently timing, start timer
        if not self.is_timing:
            self.start_time = time.time()
            self.is_timing = True
            label.text = 'timer started'  # Update text attribute of Label
        
        # If timer is running, stop timer and record time
        elif self.is_timing:
            self.end_time = time.time()
            self.is_timing = False
            self.elapsed_time = self.end_time - self.start_time
            label.text = f"{round(self.elapsed_time)}s"  # Display elapsed time
            

class TimerApp(App):
    def build(self):
        return HomeScreen()
    
if __name__ == "__main__":
    TimerApp().run()


