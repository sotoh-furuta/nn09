import win32gui
import ctypes
import win32.lib.win32con as win32con

def forground( hwnd, title):
    name = win32gui.GetWindowText(hwnd)
    if name.find(title) >= 0:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd,1) # SW_SHOWNORMAL
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        win32gui.ShowWindow(hwnd,win32con.SW_MAXIMIZE)
        # return False
        # return True


# win32gui.EnumWindows( forground, 'ETOSJX（ETOSJX）')