import colorama
from termcolor import cprint, colored
import numpy as np
import d3dshot
import time
import keyboard
import win32api
import os
import ctypes

# 初期設定
colorama.init()
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)

# 定数
KEYBIND = "alt"
BOX_LENGTH = 4
SCREEN_X = win32api.GetSystemMetrics(0)
SCREEN_Y = win32api.GetSystemMetrics(1)
REGION = (
    int(SCREEN_X/2 - BOX_LENGTH/2),
    int(SCREEN_Y/2 - BOX_LENGTH/2),
    int(SCREEN_X/2 + BOX_LENGTH/2),
    int(SCREEN_Y/2 + BOX_LENGTH/2)
)

# 管理者権限チェック
if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    cprint("管理者権限で実行してください", "red")
    exit(1)

# 画面キャプチャ初期化
d = d3dshot.create(capture_output="numpy")
win32api.GetDoubleClickTime = lambda: 0

def rgb_pixel():
    img = d.screenshot(region=REGION)
    return np.mean(img, axis=(0,1)) if img is not None else None

def click():
    win32api.mouse_event(0x0002, 0, 0, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(0x0004, 0, 0, 0, 0)

def color_match(current, target, threshold=5):
    return all(abs(c - t) < threshold for c, t in zip(current, target))

# メインループ
try:
    target_colors = [[145,94,67],[109,72,52]]
    print("準備完了...")

    while True:
        pixel = rgb_pixel()
        if pixel is not None and any(color_match(pixel, target) for target in target_colors):
            click()
            print(pixel)
            time.sleep(0.01)

except KeyboardInterrupt:
    pass

print("終了しました")
