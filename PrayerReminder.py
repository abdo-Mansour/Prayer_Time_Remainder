'''''
This project should remind the user of the prayer time and shutdown/sleep his or her PC 
to motivate them to pray in time.

API used:
    to get the current prayer times: https://aladhan.com/prayer-times-api#GetCalendarByCitys

Libraries you might use:
    for time remindrs: https://schedule.readthedocs.io/en/stable/index.html
        background: https://schedule.readthedocs.io/en/stable/background-execution.html
    for the pop up message: https://www.geeksforgeeks.org/how-to-create-a-pop-up-message-when-a-button-is-pressed-in-python-tkinter/
    for the email notification: https://www.freecodecamp.org/news/send-emails-using-code-4fcea9df63f/
    maybe add a gui if you have time: tkinter
    to make the pc go to sleep: https://stackoverflow.com/questions/37009777/how-to-make-a-windows-10-computer-go-to-sleep-with-a-python-script 
    for user locatio https://geocoder.readthedocs.io/api.html#house-addresses
    getting api requests using the requests library

''''' 

from tkinter import *
import requests
import geocoder
import json
import schedule
import time
import os


#locate the user
user_location = geocoder.ip('me')
city = user_location.city
country = user_location.country

#get prayer timings
prayer_times_response = requests.get("http://api.aladhan.com/v1/timingsByCity?"+"city="+city+"&"+"country="+country)
prayer_timings = prayer_times_response.json()['data']['timings']

prayers = {
    'Fajr':prayer_timings['Fajr'],
    'Dhuhr':prayer_timings['Dhuhr'],
    'Asr':prayer_timings['Asr'],
    'Maghrib':prayer_timings['Maghrib'],
    'Isha':prayer_timings['Isha'],
}

#########################################################################
#use input/settings
remind_only = True
force_sleep = True
time_to_force_sleep = 180
#########################################################################

def popupmsg(msg):
    '''
    This function pop up a small window to remind the user to pray.\n
    takes as input the message you want to output.

    '''
    popup = Tk()
    popup.wm_title("Prayer Time!")
    label = Label(popup, text=msg)
    label.config(font=('Helvetica bold',20))
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay, Ama go pray", font = 5 , command = popup.destroy)
    B1.pack()
    popup.mainloop()

def prayer_time():
    '''
    This function is called everytime in a prayer call.
    '''
    if(remind_only):
        popupmsg("Go Pray Brother! You have 3 minutes before your device goes to sleep.")
    
    if(force_sleep):
        time.sleep(time_to_force_sleep)
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    
#prayer times
schedule.every().day.at(prayers['Fajr']).do(prayer_time)
schedule.every().day.at(prayers['Dhuhr']).do(prayer_time)
schedule.every().day.at(prayers['Asr']).do(prayer_time)
schedule.every().day.at(prayers['Maghrib']).do(prayer_time)
schedule.every().day.at(prayers['Isha']).do(prayer_time)


#main loop
while True:
    schedule.run_pending()
    time.sleep(1)




