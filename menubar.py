
from datetime import datetime, timedelta
import rumps
rumps.debug_mode(True)

# TODO: Figure out if I can call Kivy app from here

class MenuBarIcon(rumps.App):
    def __init__(self):
        super(MenuBarIcon, self).__init__('timer')
        # Set up class variables
        self.elapsed_time = timedelta(seconds=0)
        self.is_timing = False
        self.is_reset = True
        self.ticktock = False
        # Configure app settings
        self.config = {
            'app_name': 'timer',
            'title': '●',
            'start': 'start',
            'stop': 'stop',
            'reset': 'reset',
            'quit': 'quit'
        }
        self.title = self.config['title']
        self.icon = None
        self.start_stop_button = rumps.MenuItem(title=self.config['start'], callback=self.start_stop)
        self.reset_button = rumps.MenuItem(title=self.config['reset'], callback=None)
        self.quit_button = self.config['quit']
        self.menu = [self.start_stop_button, self.reset_button]

    def start_stop(self, sender):
        """Starts or stops timer when timer button is pressed."""
        # If not currently timing, start timer
        if not self.is_timing:
            print('debug: start')
            self.is_timing = True
            self.is_reset = False
            self.start_time = datetime.now()
            self.timer_display = rumps.Timer(self.update_time, 1/2)
            self.timer_display.start()  # Update timer display
            self.update_menu()
        # If timer is running, stop timer and record time
        elif self.is_timing:
            print('debug: stop')
            self.is_timing = False
            self.is_reset = False
            self.end_time = datetime.now()
            self.elapsed_time += self.end_time - self.start_time
            self.timer_display.stop()  # Stop timer display
            self.title = self.format_time(self.elapsed_time)
            self.update_menu()

    def format_time(self, timedelta_input):
        """Takes timedelta as input and returns formatted time as H:MM."""
        total_secs = timedelta_input.total_seconds()
        hours = int(total_secs // 3600)
        mins = int((total_secs - 3600 * hours) // 60)
        secs = int((total_secs % 60) // 1)
        # Make the clock tick to show timer has started
        self.ticktock = not self.ticktock
        if self.ticktock and self.is_timing:
            return f"{hours} {mins:02}"
        else:
            return f"{hours}:{mins:02}"

    def update_time(self, *args):
        """Update timer display."""
        self.title = self.format_time(datetime.now() - self.start_time + self.elapsed_time)

    def reset_elapsed_time(self, sender):
        """If timer is not running and has not already been reset when called, reset elapsed time and hide the reset button."""
        print('debug: reset')
        self.is_timing = False
        self.is_reset = True
        self.elapsed_time = timedelta(seconds=0)
        self.timer_display.stop()  # Stop timer display
        self.title = self.config['title']  # Reset the display
        self.update_menu()

    def update_menu(self, *args):
        if self.is_timing and not self.is_reset:  # Timer is running
            print('debug: timing, not reset')
            self.start_stop_button.title = self.config['stop']
            self.reset_button.set_callback(None)
        elif not self.is_timing and not self.is_reset:  # Timer is paused
            print('debug: not timing, not reset')
            self.start_stop_button.title = self.config['start']
            self.reset_button.set_callback(self.reset_elapsed_time)
        elif not self.is_timing and self.is_reset:  # Timer is stopped and reset
            print('debug: not timing, reset')
            self.start_stop_button.title = self.config['start']
            self.reset_button.set_callback(None)


# App launcher
if __name__ == "__main__":
    MenuBarIcon().run()
