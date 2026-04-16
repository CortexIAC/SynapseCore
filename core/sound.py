import winsound

def boot_beep():
    winsound.Beep(800, 80)
    winsound.Beep(1200, 80)

def click_beep():
    winsound.Beep(1000, 40)

def error_beep():
    winsound.Beep(400, 200)