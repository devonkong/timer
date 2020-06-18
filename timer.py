import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('Program initialised.')

import kivy
kivy.require('1.11.1')

from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

import time


class HomeScreen(BoxLayout):
    pass


class TimerApp(App):
    def build(self):
        return HomeScreen()
    
    
    
if __name__ == "__main__":
    TimerApp().run()


start_time = 0
end_time = 0

def start_stopwatch():
    global start_time
    start_time = time.time()
    logging.debug(start_time)
    return start_time

def stop_stopwatch():
    global end_time
    end_time = time.time()
    logging.debug(end_time)
    return end_time

# start_stopwatch()
# time.sleep(2)
# stop_stopwatch()

# elapsed_time = end_time - start_time
# logging.debug(elapsed_time)
# formatted_time = f"Elapsed time: {round(elapsed_time)}s."

# print(formatted_time)

logging.debug('Program terminated.')