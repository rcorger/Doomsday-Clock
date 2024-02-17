from tkinter import *
import requests
from bs4 import BeautifulSoup
from PIL import ImageTk, Image

how_often_to_scan_per_hour = 120 # 120 times / 60 minutes = 2 times per min
time_types = ["seconds", "minutes", "second", "minute"]

class CurrentTime:
    def __init__(self, time_type, time):
        self.type = time_type
        self.time = time
    
    def __str__(self):
        return f"{self.time} {self.type}"


def get_doomsday_time():
    print("update called")
    time_found = False
    time_type_found = False
    ct = None

    res = requests.get("https://thebulletin.org/doomsday-clock/")
    soup = BeautifulSoup(res.text, 'html.parser')
    elements = soup.find_all("title")
    for item in elements:
        if "midnight" in item.text:
            for word in item.text.split(" "):
                if not time_found or not time_type_found:
                    if word.isdigit() and not time_found:
                        time_found = int(word)
                        continue
                    if word in time_types and not time_type_found:
                        time_type_found = word
                        #print(word, "-> time type")
                elif time_found and time_type_found:
                    ct = CurrentTime(time_type_found, time_found)
                    break

    if ct is None:
        time_lb.config(text="Time search failed :(")
        time.after(10000, get_doomsday_time) # attempt to search again after 10 seconds
    
    print(ct.__str__())
    time_lb.config(text=f"{ct.__str__()} until midnight")
    root.after(int((1000 * 60 * 60) / how_often_to_scan_per_hour), get_doomsday_time)

root = Tk()
root.title("DOOMSDAY CLOCK")
root.config(bg='lawn green')

time_lb = Label(root, text="", font=("JetBrains Mono", 30))
time_lb.config(bg='lawn green')
time_lb.pack(padx=20, pady=20)

img = ImageTk.PhotoImage(Image.open('biohazard.png'))
img_lbl = Label(root, image=img, bg="lawn green")

img_lbl.pack()

get_doomsday_time()

root.mainloop()