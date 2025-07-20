import subprocess
import pyautogui
import pygetwindow as gw
import time
import os
from PIL import Image  #
def ScreenShotGeneration():
    script_path = os.path.abspath("code_execute.py")
    process = subprocess.Popen(
        ['powershell', '-NoExit', f'python "{script_path}"'],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    time.sleep(5)
    maximized = False
    for _ in range(10):  # Retry for ~10 seconds
        time.sleep(1)
        for window in gw.getWindowsWithTitle("PowerShell"):
            if "PowerShell" in window.title and window.visible:
                window.maximize()
                maximized = True
                break
        if maximized:
            break



    time.sleep(5) 


    screenshot_path = os.path.abspath(os.path.join("userFiles", "output_image.png"))
    pyautogui.screenshot(screenshot_path)
    image = Image.open(screenshot_path)

    left = 0
    top = 50 
    right = 800
    bottom = 500 

    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save(screenshot_path)
    pyautogui.hotkey('alt', 'f4')
