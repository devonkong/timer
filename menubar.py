
from datetime import datetime, timedelta
import rumps
rumps.debug_mode(False)

# TODO: Figure out if I can call Kivy app from here
# TODO: Implement project tracking
# TODO: Pomodoro timer / reminders to take breaks
# TODO: Configure different time layouts

class MenuBarIcon(rumps.App):
    def __init__(self):
        super(MenuBarIcon, self).__init__('Timer')
        # Set up class variables
        self.elapsed_time = timedelta(seconds=0)
        self.is_timing = False
        self.is_reset = True
        self.ticktock = False
        self.hide_timer = False
        # Configure app settings
        self.config = {
            'app_name': 'Timer',
            'title': '⧗',
            'start': 'Start',
            'stop': 'Stop',
            'reset': 'Reset',
            'settings': 'Settings',
            'show_timer': 'Show elapsed time',
            'hide_timer': 'Hide elapsed time',
            'quit': 'Quit'
            }
        self.title = self.config['title']
        self.icon = None
        self.start_stop_button = rumps.MenuItem(title=self.config['start'], callback=self.start_stop)
        self.reset_button = rumps.MenuItem(title=self.config['reset'], callback=None)
        self.settings_button = rumps.MenuItem(title=self.config['settings'], callback=None)
        self.hide_timer_button = rumps.MenuItem(title=self.config['hide_timer'], callback=self.show_hide_timer)
        self.quit_button = self.config['quit']
        self.menu = [
            self.start_stop_button,
            self.reset_button,
            [self.settings_button, [self.hide_timer_button]]
            ]

    def start_stop(self, *args):
        """Starts or stops timer when timer button is pressed."""
        # If not currently timing, start timer
        if not self.is_timing:
            print('debug: start')
            self.is_timing = True
            self.is_reset = False
            self.start_time = datetime.now()
            self.timer_display = rumps.Timer(self.update_time, 1)
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
            return f"{hours:02} {mins:02}"
        else:
            return f"{hours:02}:{mins:02}"

    def update_time(self, *args):
        """Update timer display."""
        if not self.hide_timer:
            self.title = self.format_time(datetime.now() - self.start_time + self.elapsed_time)
        else:
            # If hide_timer = True, blink icon to show that timer is running
            self.ticktock = not self.ticktock
            if self.ticktock and self.is_timing:
                self.title = '⧗'
            else:
                self.title = '⧖'

    def reset_elapsed_time(self, *args):
        """If timer is not running and has not already been reset when called, reset elapsed time and hide the reset button."""
        print('debug: reset')
        self.is_timing = False
        self.is_reset = True
        self.elapsed_time = timedelta(seconds=0)
        self.timer_display.stop()  # Stop timer display
        self.title = self.config['title']  # Reset the display
        self.update_menu()

    def show_hide_timer(self, *args):
        """Show or hide elapsed time in the menu bar and update hide_timer_button based on user settings."""
        print('debug: show/hide')
        self.hide_timer = not self.hide_timer
        self.update_menu()


    def update_menu(self, *args):
        """Update menu items depending on timer status and user settings."""
        # Update start, stop and reset buttons
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
        # Update show/hide timer button
        if self.hide_timer:  # Hide timer is selected
            print('debug: hide timer')
            self.hide_timer_button.title = self.config['show_timer']
        elif not self.hide_timer:  # Show timer is selected
            print('debug: show timer')
            self.hide_timer_button.title = self.config['hide_timer']


# App launcher
if __name__ == "__main__":
    MenuBarIcon().run()
