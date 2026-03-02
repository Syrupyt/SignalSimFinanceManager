# SignalSimFinanceManager
  A manager program that takes in all purchased Upgrades and calculates three things: credits needed to unlock the rest, credits already spent, and percent complete.


## Saving:
  Saves to a savedata.json in the directory you put the executable in.
  
  ⚠️ WARNING: IF MOVING EITHER OF THESE FILES, MOVE THEM TOGETHER. OTHERWISE A NEW SAVE FILE WILL BE CREATED, AND IT'LL BE SET TO ZERO
  
  The best thing about this? It doesn't use your personal files:
    on Linux, it's usually ~/.local/share or ~/.config
    on Windows, it's usually in Appdata or Documents.
  This program doesn't do that. The *only* files affected is the folder you run the program in. So the only uninstall steps? Just delete the executable, and the json.
  
  Do note, I haven't tested shortcuts, and they may break due to my use of os.path. Though try it out and see.

## Features:
  Upgrade details; click on any of the icons and see a (fairly) detailed explanation of the upgrade and what it does. If there's anything off about my data, go ahead and make an Issues ticket on this repository. Though don't expect it to be updated quickly, I aint switching operating systems and running pyinstaller every time I make a mistake on a non-essential part of the program.
  
  Saving; Obviously, can save. Saves to a very easily interpretable savedata.json file which is literally just a list of the modules with the numbers. Literally nothing else.
  Reset; Reset button does what it says; when you click it (with a warning), it zeros out the savedata.json. Deleting said file does the same thing.
    Note: Closing the program does not automatically save, nor lets you know that it hasn't been saved. Be careful when closing.
  
  Finance calculation; My favourite. It calculates not just the cost to advance the current tier, but calculates the cost it would take to get all the way to the max tier. While I could code a way to see the remaining cost of each module separately when clicked, but I'm too lazy to do that. Though, who knows, maybe I'll get interested again. Shows total, total spent, total needed to complete, and percent completed. Live updates.


## Installation:
  Windows:
    Download SigSimFinanceManager{version}-win.exe
    Put it in any directory you choose
    Run it like any other .exe
  Linux:
    Download SigSimFinanceManager{version}-lin
    Put it in any directory you choose
    Run it like any other executable (may need to do the command 'chmod +x path/to/your/dir/SigSimFinanceManager{version}-lin')





## For developers:
  If you wish to modify this in any way, simply download the directory as a zip, and open it like any regular Python program. Visual Studio Code recommended, but you choose your seasoning. I'll allow any branch requests (if I can figure out how, github is freaky).
  
  Needed packages (most are pre-installed):
    -tkinter
    -os
    -sys
    -json
    -shutil
    
  Also, sorry for the severe lack of comments in my code!
