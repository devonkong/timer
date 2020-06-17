import time, datetime
import threading


def stopwatch():
    
    input("Press ENTER to start.")
    start_time = time.time()

    input("Press ENTER to stop.")
    end_time = time.time()

    elapsed_time = end_time - start_time
    formatted_time = f"Elapsed time: {round(elapsed_time)}s."
    
    return formatted_time


print(stopwatch())