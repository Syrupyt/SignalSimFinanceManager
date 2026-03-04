import tkinter as tk
from tkinter import ttk
import json
import os
import sys
import shutil

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(".")

sub_nine = False

def cost(levels):
    global sub_nine
    out = []
    for level in levels:
        out.append(sum(
            (30 + 45*l - (10 if l == 9 and sub_nine else 0))
            for l in range(level, 10)
        ))
    return sum(out)

# Total variable (already calculated)
total = 48825  

# ----- Config -----
json_default = resource_path("savedata.json")
json_save = os.path.join(app_dir(), "savedata.json")

bottom_text_presets = [
    "Azimuth:\n\nAffects the speed of the antenna's spin. Starts out at 0.0080 (from old versions at the least, not sure if it applies today, 0.0100 makes more sense), but can get as high as 0.0300 (0.0390 when antennas are boosted).\n\n It is unknown what this number means, but it's likely some sort of fraction of a degree over some unit of time.\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 0.0100\nIncrements by: 0.0020\nEnds at: 0.0300", 
    
    "Antenna detection:\n\nIncreases the allowed error before seeing a signal on the Signal Strength Meter. Affects both azimuth and elevation detection in the same way.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 0.4\nIncrements by: 0.02\nEnds at: 0.6", 
    
    "Tracking:\n\nI wouldn't really call this 'tracking', more like 'automation'.\nIt's relating to the 'Auto-Scan' and 'Track Signal' buttons on the Frequency Scanner panel (bottom center) and the Antenna Controls panel (slight right).\nIt decreases the cost of Electronics (the resource spent when pressing said buttons), which means this is pretty much only an Ease of Use upgrade. Get this if you're lazy.\n\nIn game without context, this one can be hard to understand.\n\n\n\n\n\n\n\n\n\nStarts at: 100% \nIncrements by: -5% \nEnds at: 50%",
    
    "Coordinates:\n\nDecreases the amount of error when scanning for coordinates. Helps a ton when you struggle with finding signals.\n\nThough, here's my strategy for finding signals:\n\nGo to the average. If there is nothing, add 1 and move. Keep going untill you reach about 2/3 the way to the maximum. Then, go back to the average and subtract 1, then move. Keep doing that untill you again reach 2/3 to the minimum. This strategy has worked out great for me.\n\n\n\n\n\n\n\n\n\nStarts at: 20.0 \nIncrements by: -0.4 \nEnds at: 16", 
    
    "Elevation:\n\nAffects the speed of the antenna's pitch. Pretty much the same as Azimuth. Upgrade Azimuth before this, though; more distance to travel.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 0.0100\nIncrements by: 0.0020\nEnds at: 0.0300", 
    
    "Coordinate buffer:\n\nOne of the most important upgrades. Starts out at 10 and ends at 20, with 1 upgrade per slot.\n\nThe reason this upgrade is so important is how much it increases your chances that the signal will be at the predicted coordinates, ironically much more than the Coordinates upgrade. Get this BEFORE getting coordinate upgrades.\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 10\nIncrements by: 1\nEnds at: 20",
    
    "Cooling:\n\nSimply decreases the rate that the servers heat up. Not much to explain, not much to not understand.\n\nAbout server temperature:\nVisible via the command 'tempcheck', or by looking at the Server Temperature on the main menu. A good rule of thumb is to run 'turbo' whenever the temperature raises above 50 degrees.\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarts at:100% \nIncrements by:-2.5% \nEnds at:75%",
     
    "Download:\n\nOne of the most important upgrades. Caps at 8mb/s, but can be increased to ~10mb/s with the Power Distributor.\n\nTip: You can see if servers are down in 4 ways: with the command 'diagnostics' in the terminal, looking at the download speed on the Download screen and seeing it's halved, looking at the download speed on the front screen and seeing it's halved, and lastly (and most conveniently), looking at the very left top monitor, that says 'services'. If it says 'running', you're all good. If it says 'error', go into the terminal and type 'rebootall'. Instead of waiting for that to finish, close the terminal immediately and look back up at the monitor. If it's fixed, tada. If it's not, go back into terminal and find the errored antenna, and go reboot it manually.\n\n\nStarts at: 4.0mb/s \nIncrements by: 0.4mb/s \nEnds at: 8.0mb/s", 
    
    "Module maintenance:\n\nDecreases the cost required to maintain modules. Amazing for people who use modules a lot.\n\nTip: If you're wondering why you aren't gaining as much money as you should, then check your modules and add up the maintenance earning cost %. Then multiply that by the percent of this upgrade. That's how many credit's you're currently missing out on. This can get very high, and why I personally don't use modules.\n \n \n \n \n \n \n \n\n\n\n\nStarts at: 100%\nIncrements by: 5%\nEnds at: 50%",
    
    "Generator efficiency:\n\nAn interesting quirk about the generator is that it doesn't actually generate electricity. All it does is increase the incoming power and multiply it by a percent. It will not work at night, because 0 multiplied by anything is 0.\n\nI personally don't use the generator much, as I have recharge rate and efficiency maxed, meaning my system efficiency never goes below 70, even in the night.\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 25%\nIncrements by: 2.5%\nEnds at: 50%", 
    
    "Recharge rate:\n\nOne of the most important upgrades in the game, and I don't even need to explain why. Increases rate of recharge. If you max this out, you don't even really need to care about system efficiency because it's just gonna go right back up in the day even while doing signals *and* boinc.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 100%\nIncrements by: 2.5%\nEnds at: 125%", 
    
    "UPS:\n\nOne of the least useful upgrades there is, and if you've ever got a lightning storm, you would agree with me. Power outages do absolutely nothing but make it so you can't see screens (not panels) for a couple seconds. And the chance of lighting causing an outage is already so low that it isn't all that annoying. Only get this if it really nags at you.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 10%\nCost function: -(100/x+10)%, x=lvl\nEnds at: 5%",
    
    "Calibration offset:\n\nSlows the rate at which the antenna calibration becomes offset. Fairly useful if you don't like calibrating the antennas, though not required in the slighest; without it, it still takes a very long time for calibration to actually have a negative effect.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 100%\nIncrements by: 5%\nEnds at: 50%", 
    
    "Energy distribution:\n\nArguably the worst upgrade there is.\n\n\nAll it does...\n\nIs make it so, when you distribute power...\n\nThe systems you AREN'T using...\n\nWaste all your power!\n\n\nFantastic! Amazing!\n\n\n\n\n\n\nif you get this you're either stupid or maxing out all the upgrades.\n\n\nStarts at: 0%\nIncrements by: 2%\nEnds at: 20%", 
    
    "Boinc Gen:\n\nIncreases the chance that a sucessful Boinc program finish will result in a module. Do note that it's smart to save what modules you have if you want to see if it was sucessful or not, as I'm not sure there is any indication otherwise. Starts at 5% chance, increments by 1%, ending at 15%.\n\nTip: Always run boinc in the day. Never in the night, but *always* in the day. If of course you care about modules, which in that case you can ignore this.\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 100%\nIncrements by: 2.5%\nEnds at: 75%",
    
    "Boinc speed:\n\nIncreases the speed that a Boinc program will finish. Useful if you often use modules. and don't want to deal with the insane downsides.\n \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 100%\nIncrements by: 5%\nEnds at: 150%", 
    
    "Auto-calibration speed:\n\nIncreases the speed at which the sattelites are calibrated when using 'calstart'.\n\n General calibration info:\nEven when maxed, auto calibration will still take a decent while, so it is reccomended to use command 'service' to be able to manually calibrate the antennas. Work down the sattelites, starting at Satellite 19 and going down numerically. Run autocalibration alongside your manual calibration to maximize effectiveness.\n\nNote: It is reccomended to only calibrate when the offset is above 10 (which is easily identifiable when the text turns red in the terminal when checking calibration).It's also not a crazy issue to ignore it for a while, as I haven't seen any too averse effects from a high calibration error.\n\nStarts at: 100%\nIncrements by: 10%\nEnds at: 200%", 
    
    "System efficiency:\n\nOne of the most important upgrades. Lowers the rate at which system efficiency goes down at night, and indirectly increases recharge rate.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 100%\nIncrements by: 2.5%\nEnds at: 75%",
    
    "Rover speed:\n\nIncreases the speed that the Rover moves. Not very hard to understand, dunno why you're looking here.\n\nThough, tip: use the rover whenever possible. It's semi-autonomous, and you get 150 credits every meteor you scan. If you can't find said meteor, that's fine, but there's nothing wrong with an extra 150.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 0.30m/s\nIncrements by: 0.03m/s\nEnds at: 0.60m/s", 
    
    "Rover analyze speed:\n\nIncreases the speed of the rover's analyzer. If you don't know what this means, don't use the rover.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 100%\nIncrements by: 10%\nEnds at: 200%",
     
    "Polarization speed:\n\nI *think* this one refers to the speed at which the slider moves when first getting a signal. Though I'm not sure. Lemme know with a github Issues ticket at github.com/syrupyt/SignalSimFinanceManager/issues.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nStarts at: 100%\nIncrements by: 10%\nEnds at: 200%"
]


json_presets = [
    "Azimuth", 
    "Antenna detection", 
    "Tracking",
    "Coordinates", 
    "Elevation", 
    "Buffer",
    "Cooling", 
    "Download", 
    "Modules",
    "Generator", 
    "Recharge", 
    "UPS",
    "Offset", 
    "Distribution", 
    "BGen",
    "BSpeed", 
    "Calibration", 
    "Efficiency",
    "RSpeed", 
    "Analyze", 
    "Polarization"
]




# ----- Load saved data -----
if not os.path.exists(json_save):
    shutil.copy(json_default, json_save)
    
with open(json_save, "r") as f:
    saved_data = json.load(f)


# ----- CounterBox Class ----- #
class CounterBox:
    def __init__(self, master, key, icon_image=None, bottom_label=None, update_cost_label=None):
        self.key = key
        self.number = saved_data.get(key, 0)
        self.bottom_label = bottom_label
        self.update_cost_label = update_cost_label
        self.frame = tk.Frame(master, padx=5, pady=5, bd=2, relief="solid")

        # Icon
        if icon_image:
            self.icon = tk.Label(self.frame, image=icon_image)
            self.icon.image = icon_image
        else:
            self.icon = tk.Label(self.frame, text="🗂", font=("Arial", 24))
        self.icon.grid(row=0, column=0, columnspan=3, pady=(0,5))
        self.icon.bind("<Button-1>", self.update_bottom_text)

        # Buttons and number
        self.minus = tk.Button(self.frame, text="-", width=3, command=self.decrease)
        self.minus.grid(row=1, column=0)

        self.label = tk.Label(self.frame, text=str(self.number), width=3)
        self.label.grid(row=1, column=1)

        self.plus = tk.Button(self.frame, text="+", width=3, command=self.increase)
        self.plus.grid(row=1, column=2)

        self.frame.pack_propagate(False)

    def increase(self):
        if self.number < 10:
            self.number += 1
            self.label.config(text=str(self.number))
            self.update_cost()

    def decrease(self):
        if self.number > 0:
            self.number -= 1
            self.label.config(text=str(self.number))
            self.update_cost()

    def update_bottom_text(self, event=None):
        if self.bottom_label:
            index = counter_boxes.index(self)
            total_selected = cost([self.number])
            self.bottom_label.config(text=bottom_text_presets[index] + f"\n\n\nTotal cost to complete {json_presets[index]} upgrade: {total_selected}")

    def update_cost(self):
        if self.update_cost_label:
            numbers = [box.number for box in counter_boxes]
            c = cost(numbers)
            percent = round(((total - c)/total) * 100, 5)
            text = f"Cost required to complete: {c}\n\nTotal: {total}\n\nTotal spent: {total - c}\n\n% Complete: {percent}%"
            self.update_cost_label.config(text=text)
            index = counter_boxes.index(self)
            total_selected = cost([self.number])
            self.bottom_label.config(text=bottom_text_presets[index] + f"\n\n\nTotal cost to complete {json_presets[index]} upgrade: {total_selected}")

# ----- Save Function -----
def save_data():
    data = {box.key: box.number for box in counter_boxes}
    with open(json_save, "w") as f:
        json.dump(data, f, indent=4)
    
# ----- Reset Function ----- #
def reset_data():
    if reset_button.cget('text') == "Reset":
        reset_button.config(text='Are you sure?')
    elif reset_button.cget('text') == 'Are you sure?':
        data = {key:0 for key in json_presets}
        with open(json_save, "w") as f:
            json.dump(data, f, indent=4)
        reset_button.config(text="Reset complete: restart to show effects")

# ----- GUI -----
root = tk.Tk()

icon_files = [
    resource_path(os.path.join("icons", f"{i}.png"))
    for i in range(1, 22)
]

icon_images = [
    tk.PhotoImage(file=f)
    for f in icon_files
]

root.title("Signal Simulator Finance Manager")

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

# Left: counter grid
grid_frame = tk.Frame(main_frame)
grid_frame.grid(row=0, column=0, padx=(0,10))

rows, cols = 7, 3  # vertical
counter_keys = list(saved_data.keys())
counter_boxes = []

for r in range(rows):
    for c in range(cols):
        idx = r*cols + c
        if idx >= len(counter_keys):
            break
        box = CounterBox(grid_frame, key=counter_keys[idx], icon_image=icon_images[idx])
        box.frame.grid(row=r, column=c, padx=5, pady=5)
        counter_boxes.append(box)

# Vertical separator
vert_sep = ttk.Separator(main_frame, orient="vertical")
vert_sep.grid(row=0, column=1, sticky="ns", padx=5)

# Right: text area
text_frame = tk.Frame(main_frame)
text_frame.grid(row=0, column=2, sticky="n")

# Top box: dynamic cost info
cost_label = tk.Label(text_frame, text="", justify="left", anchor="nw", font=("Arial", 10), bd=2, relief="solid", padx=5, pady=5, width=30)
cost_label.pack(fill="both", expand=True, pady=(0,10))

#Separator
horz_sep = ttk.Separator(text_frame, orient="horizontal")
horz_sep.pack(fill='both', expand=True, pady=10)

# Bottom dynamic text
bottom_label = tk.Label(text_frame, text="Click an icon to show info here", justify="left", anchor="nw", width=30, wraplength=240)
bottom_label.pack(fill="x")

# Link bottom label and cost_label to all boxes
for box in counter_boxes:
    box.bottom_label = bottom_label
    box.update_cost_label = cost_label
    box.update_cost()  # initialize display

# Save button
save_button = tk.Button(root, text="Save", command=save_data)
save_button.pack(pady=10)

#Reset button
reset_button = tk.Button(root, text="Reset", command=reset_data)
reset_button.place(relx=0.01, rely=0.9875, anchor='sw')

#Credits text
credits = tk.Label(root, text='Created by Okamiashi', justify='left', anchor='nw')
credits.place(relx=0.8, rely=0.985, anchor='sw')

root.mainloop()