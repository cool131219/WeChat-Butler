"""
打开微信 — 通过任务栏绿色图标点击唤醒
如果微信不在运行，自动启动后再找图标点击
Usage: python scripts/open_wechat.py
"""
import pyautogui
import pygetwindow as gw
import time
import sys
import os
import subprocess

WEI_COLOR = (7, 193, 96)  # #07C160
TOLERANCE = 40
MAX_ATTEMPTS = 20
RETRY_DELAY = 1.5
WEIXIN_PATH = os.path.expandvars(r'%ProgramFiles%\Tencent\Weixin\Weixin.exe')
TASKBAR_H = 48


def find_wechat_icon():
    """截图任务栏 → 返回(center_x, center_y) 或 None"""
    screen_w, screen_h = pyautogui.size()
    taskbar_y = screen_h - TASKBAR_H

    s = pyautogui.screenshot(region=(0, taskbar_y, screen_w, TASKBAR_H))
    green_pixels = {}
    for y in range(TASKBAR_H):
        for x in range(screen_w):
            r, g, b = s.getpixel((x, y))
            if (abs(r - WEI_COLOR[0]) < TOLERANCE and
                abs(g - WEI_COLOR[1]) < TOLERANCE and
                abs(b - WEI_COLOR[2]) < TOLERANCE):
                green_pixels.setdefault(x, []).append(y)

    if not green_pixels:
        return None

    sorted_x = sorted(green_pixels.keys())
    clusters = []
    start_x = sorted_x[0]
    prev_x = start_x

    def flush_cluster():
        nonlocal start_x, prev_x
        ys = []
        for xx in range(start_x, prev_x + 1):
            ys.extend(green_pixels.get(xx, []))
        width = prev_x - start_x + 1
        height = max(ys) - min(ys) + 1 if ys else 0
        if width > 15 and height > 15:
            cx = (start_x + prev_x) // 2
            cy = taskbar_y + (min(ys) + max(ys)) // 2
            clusters.append((cx, cy))

    for x in sorted_x[1:]:
        if x - prev_x > 3:
            flush_cluster()
            start_x = x
        prev_x = x
    flush_cluster()

    return clusters[0] if clusters else None


def is_wechat_open():
    wins = gw.getWindowsWithTitle('微信')
    return bool(wins) and wins[0].visible and not wins[0].isMinimized

def is_wechat_foreground():
    """检查微信是否在最前面（活动窗口）"""
    try:
        active = gw.getActiveWindow()
        return active is not None and '微信' in active.title
    except Exception:
        return False


def launch_wechat():
    """启动微信进程"""
    if os.path.exists(WEIXIN_PATH):
        subprocess.Popen([WEIXIN_PATH])
        print(f"  launched: {WEIXIN_PATH}")
        time.sleep(3)  # 等窗口出现
        return True
    else:
        print(f"  wechat not found at: {WEIXIN_PATH}")
        return False


def open_wechat():
    # Step 1: 先检查窗口是否已在
    if is_wechat_open():
        print("✓ 微信已在前台")
        return True

    # Step 2: 检查任务栏有没有图标
    pos = find_wechat_icon()
    if not pos:
        print("→ 任务栏没有微信图标，尝试启动微信...")
        if not launch_wechat():
            print("✗ 无法找到微信程序")
            return False
        # 启动后再找图标
        for _ in range(5):
            pos = find_wechat_icon()
            if pos:
                break
            time.sleep(1)

    # Step 3: 点击图标（最多重试20次）
    for attempt in range(1, MAX_ATTEMPTS + 1):
        if not pos:
            pos = find_wechat_icon()
        if pos:
            pyautogui.click(pos[0], pos[1])
        time.sleep(RETRY_DELAY)
        if is_wechat_open():
            if is_wechat_foreground():
                print(f"✓ 微信已打开并在最前面 (attempt {attempt})")
                return True
            else:
                # 窗口存在但不是最前面，再点一次任务栏图标让它浮上来
                print(f"  → 微信窗口在后面，再点一次图标 (attempt {attempt})")
                if pos:
                    pyautogui.click(pos[0], pos[1])
                time.sleep(1)
                if is_wechat_foreground():
                    print(f"✓ 微信已浮到最前面")
                    return True
                # 还不成功就继续重试
        pos = None  # 下次重新找

    print("✗ 没有打开")
    return False


if __name__ == "__main__":
    success = open_wechat()
    sys.exit(0 if success else 1)
