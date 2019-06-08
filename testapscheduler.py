import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

print("1")
scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=5)
scheduler.start()
print('2')

# use python3 -i testapscheduler.py 


# Shut down the scheduler when exiting the app
#atexit.register(lambda: scheduler.shutdown())