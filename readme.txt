プリンタードライバー Generic / Text Only （windowsに内蔵）をインストールする。
Generic / Text Onlyを既定のプリンターに変更。
プリンターの設定を日本語に変更。

ETOSのDELETEキーに全消去を割り当て

_pyautogui_win.py を編集する。

    needsShift = pyautogui.isShiftCharacter(key)
	↓
    needsShift = pyautogui.isShiftCharacter(key)
    if key == '@': needsShift = False
    if key == '^': needsShift = False
    if key == ':': needsShift = False