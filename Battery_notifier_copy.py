import time
from plyer import notification
import psutil
import pyttsx3
import tkinter as tk
import threading

def speak(text):
    engine=pyttsx3.init()
    engine.setProperty('rate',130)
    engine.setProperty('volume',8)
    engine.say(text)
    engine.runAndWait()

def monitor():
    #used a global variable so that this variable is available to both start and stop function
    global running # use a global variable to control the loop    
    while running:
        time.sleep(10)
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = int(battery.percent)

        if percent < 95:
            if plugged==False:
                notification.notify(
                    title = "Battery Reminder",
                    message = "Your battery is running low. You might want to plug."
                )
                speak("Your battery is running low. You might want to plug.")  
        if percent == 80:
            if plugged ==True:
                notification.notify(
                    title = "Plugged In",
                    message = "Your battery is 80%. You might want to plug out."
                )
                speak("Your battery is 80%. You might want to plug out. ")
        elif percent >=90:
            if plugged ==True:
                notification.notify(
                    title = "Plugged In",
                    message ="Your battery almost fully charged. You might want to plug out."
                )
                speak("Your battery almost fully charged. You might want to plug out.")

def start():
    global running # use a global variable to control the loop
    running = True # set it to True when the play button is clicked
    t = threading.Thread(target=monitor) # create a thread for the monitor function
    t.start() # start the thread

    status.config(text="Running!")#update status bar on push of button
    status.update()
    

def stop():
    global running # use a global variable to control the loop
    running = False # set it to False when the stop button is clicked
    status.config(text="Stopped :(")#update status bar on push of button
    status.update()

# create a tkinter window
window = tk.Tk()
window.title("Battery Monitor")
window.geometry("300x200")

# create a play button
play_button = tk.Button(window, text="Start", command=start,activebackground='black',activeforeground='white')
play_button.pack()

# create a stop button
stop_button = tk.Button(window, text="Stop", command=stop)
stop_button.pack()

status=tk.Label(window,text="Running")
status.pack(side="bottom",anchor="center",fill="x")
# start the main loop of the window
window.mainloop()
