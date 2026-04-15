# ETOS prn出力モジュール

# logging　config
from logging import getLogger, config
import json
with open('./log_config.json', 'r') as f:
    log_conf = json.load(f)
config.dictConfig(log_conf) #ロギング設定を取得
logger = getLogger(__name__)  #アプリ名でロギング
# logging　config END


# import
import pyautogui
from active2 import forground
import win32gui
import subprocess
import time
import pyperclip



def ETOS_OPEN(TEMP_DIR):

    #ETOS起動 START

    logger.debug('ETOS open')
    # subprocess.Popen(r'C:\Program Files (x86)\ETOSJX\wnetos.exe "C:\Program Files (x86)\ETOSJX\ETOSJX.PG"')
    p = subprocess.Popen(r'C:\Program Files (x86)\ETOSJX\wnetos.exe ETOSJX.PG')

    time.sleep(1)
    # ETOS画面を最前面に
    win32gui.EnumWindows( forground, 'ETOSJX（ETOSJX）')
    pyautogui.click(20,5, button="left")
    time.sleep(1)

    # ETOS起動 END
    ###########################################################
    # 09画面読み込み START

    pyperclip.copy("AA0090")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press("F12")
    time.sleep(0.3)
    pyautogui.press("F9")
    time.sleep(0.3)
    pyperclip.copy(TEMP_DIR + "aa09")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press("enter")
    time.sleep(0.1)
    pyautogui.press("y")
    logger.debug(TEMP_DIR + "aa09.prn output")
    # 09画面読み込み END
    ###########################################################
    # CC09画面読み込み START

    time.sleep(0.3)
    pyautogui.press("delete")
    time.sleep(0.3)
    pyperclip.copy("CC0090")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press("F12")
    time.sleep(0.3)
    pyautogui.press("F9")
    time.sleep(0.3)
    pyperclip.copy(TEMP_DIR + "cc09")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press("enter")
    time.sleep(0.1)
    pyautogui.press("y")
    logger.debug(TEMP_DIR + "cc09.prn output")

    # CC09画面読み込み END
    ###########################################################
    # NN09画面読み込み START

    time.sleep(0.3)
    pyautogui.press("delete")
    time.sleep(0.3)
    pyperclip.copy("NN0090")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press("F12")
    time.sleep(0.3)
    pyautogui.press("F9")
    time.sleep(0.3)
    pyperclip.copy(TEMP_DIR + "nn09")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press("enter")
    time.sleep(0.1)
    pyautogui.press("y")
    logger.debug(TEMP_DIR + "nn09.prn output")

    # NN09画面読み込み END
    ###########################################################
    # AD0291画面読み込み START

    time.sleep(0.3)
    pyautogui.press("delete")
    time.sleep(0.3)
    pyperclip.copy("AD0291")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press("F12")
    time.sleep(0.3)
    pyautogui.press("F9")
    time.sleep(0.3)
    pyperclip.copy(TEMP_DIR + "ad291")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press("enter")
    time.sleep(0.1)
    pyautogui.press("y")
    logger.debug(TEMP_DIR + "ad291.prn output")

    # AD291画面読み込み END
    ###########################################################
    # 3K画面読み込み START

    time.sleep(0.3)
    pyautogui.press("delete")
    time.sleep(0.3)
    pyperclip.copy("AA03K2")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press("F12")
    time.sleep(7)
    pyautogui.press("F9")
    time.sleep(0.3)
    pyperclip.copy(TEMP_DIR + "aa3k")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press("enter")
    time.sleep(0.1)
    pyautogui.press("y")
    logger.debug(TEMP_DIR + "aa3k.prn output")

    # 3K画面読み込み END
    ###########################################################
    # NN3L画面読み込み START

    time.sleep(0.3)
    pyautogui.press("delete")
    time.sleep(0.3)
    pyperclip.copy("NN03L0")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press("F12")
    time.sleep(7)
    pyautogui.press("F9")
    time.sleep(0.3)
    pyperclip.copy(TEMP_DIR + "nn3l")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press("enter")
    time.sleep(0.1)
    pyautogui.press("y")
    logger.debug(TEMP_DIR + "nn3l.prn output")

    #NN3L画面読み込み END
    ###########################################################
    # ETOS close

    time.sleep(1)
    pyautogui.hotkey("ALT","F4")
    pyautogui.press("Y")
    logger.debug('ETOS closed.')

    # ETOS closed
    return p
