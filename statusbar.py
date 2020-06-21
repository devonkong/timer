from datetime import datetime, timedelta
import rumps

# TODO: Figure out how to show started/stopped/reset (blinking text?)
# TODO: Icon for statusbar
# TODO: Update display to show HH:MM
# TODO: Figure out if I can call Kivy app from here


class StatusBarWidget(rumps.App):
    elapsed_time = timedelta(seconds=0)
    is_timing = False

    def __init__(self):
        super(StatusBarWidget, self).__init__('timer')
        self.title = 'timer'
        self.quit_button = 'quit'

    @rumps.clicked('start')
    def start_stop(self, *args):
        """Starts or stops timer when timer button is pressed."""
        # If not currently timing, start timer
        if not self.is_timing:
            print('debug: start')
            self.is_timing = True
            self.start_time = datetime.now()
            self.menu['start'].title = 'stop'
            self.timer_display = rumps.Timer(self.update_time, 1)
            self.timer_display.start()  # Update timer display
        # If timer is running, stop timer and record time
        elif self.is_timing:
            print('debug: stop')
            self.is_timing = False
            self.end_time = datetime.now()
            self.elapsed_time += self.end_time - self.start_time
            self.timer_display.stop()  # Stop timer display
            self.title = '~' + self.format_time(self.elapsed_time)
            self.menu['start'].title = 'start'
            self.reset_elapsed_time.stop

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
        print('debug: update display')
        self.title = self.format_time(datetime.now() - self.start_time + self.elapsed_time)

    @rumps.clicked('reset')
    def reset_elapsed_time(self, *args):
        """If timer is not running and has not already been reset when called, reset elapsed time and hide the reset button."""
        print('debug: reset')
        self.is_timing = False
        self.elapsed_time = timedelta(seconds=0)
        self.menu['start'].title = 'start'
        self.timer_display.stop()  # Stop timer display
        self.title = 'timer'  # Reset the display


# App launcher
if __name__ == "__main__":
    StatusBarWidget().run()
