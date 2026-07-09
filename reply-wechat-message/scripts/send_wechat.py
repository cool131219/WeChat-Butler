"""
发送微信消息到指定联系人
用法 / Usage:
  python send_wechat.py <联系人> [消息内容]    # 命令行参数 / command-line arg
  echo "消息内容" | python send_wechat.py <联系人>  # stdin管道（推荐）/ stdin pipe (recommended)

如果省略消息内容，只打开聊天页面
If message is omitted, just opens the chat page.

流程 / Flow:
  1. 确保微信在前台 / Ensure WeChat is in foreground
  2. 点击侧边聊天标签 / Click chat tab in sidebar
  3. 点击聊天列表中的目标对话 / Click the target contact in chat list
  4. 发送消息 / Send message
"""
import pyautogui, pygetwindow as gw, time, pyperclip, os, subprocess, sys

pyautogui.FAILSAFE = False

# === 常量 / Constants ===
SEARCH_X_REL = 90   # 搜索框x偏移 / Search box x offset
SEARCH_Y_REL = 60   # 搜索框y偏移 / Search box y offset
CHAT_TAB_X = 41     # 聊天标签x偏移 / Chat tab x offset (from window left)
CHAT_TAB_Y = 130    # 聊天标签y偏移 / Chat tab y offset (from window top)
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
OPEN_SCRIPT = os.path.join(SCRIPTS_DIR, 'open_wechat.py')


def bring_wechat_foreground(w):
    """Bring WeChat window to foreground"""
    if w.isMinimized:
        w.restore()
        time.sleep(0.5)
    try:
        w.activate()
    except:
        pass
    time.sleep(1)
    try:
        import ctypes
        user32 = ctypes.windll.user32
        hwnd = w._hWnd
        user32.SetForegroundWindow(hwnd)
        time.sleep(0.5)
    except:
        pass


def ensure_wechat():
    """确保微信在前台 / Ensure WeChat is in foreground"""
    wins = gw.getWindowsWithTitle('微信')
    if not wins:
        print("→ 微信未运行，启动中... / WeChat not running, starting...")
        subprocess.run(['python', OPEN_SCRIPT], capture_output=True, text=True, timeout=60)
        time.sleep(2)
        wins = gw.getWindowsWithTitle('微信')
        if not wins:
            print("失败：无法打开微信 / Failed to open WeChat")
            return False

    w = wins[0]
    bring_wechat_foreground(w)
    return True


def click_chat_tab():
    """点击侧边聊天图标，确保在聊天页面 / Click chat tab in sidebar"""
    for _ in range(5):
        wins = gw.getWindowsWithTitle('微信')
        if not wins:
            continue
        w = wins[0]
        pyautogui.click(w.left + CHAT_TAB_X, w.top + CHAT_TAB_Y)
        time.sleep(0.3)


def search_and_open(name):
    """搜索联系人并打开聊天 / Search contact and open chat"""
    click_chat_tab()
    time.sleep(0.5)

    wins = gw.getWindowsWithTitle('微信')
    if not wins:
        return False
    w = wins[0]
    left, top = w.left, w.top

    # 点搜索框 / Click search box
    pyautogui.click(left + 60 + SEARCH_X_REL, top + SEARCH_Y_REL)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    time.sleep(0.3)

    pyperclip.copy(name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    pyautogui.press('enter')
    time.sleep(2)
    return True


def send_message(msg):
    """在已打开的聊天窗口输入并发送消息 / Type and send message in open chat"""
    pyperclip.copy(msg)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1)
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法 / Usage:")
        print("  python send_wechat.py <联系人/contact> [消息/message]")
        print("  echo '消息/message' | python send_wechat.py <联系人/contact>")
        sys.exit(1)

    contact = sys.argv[1]

    # 消息来源 / Message source: 命令行参数 > stdin管道
    message = None
    if len(sys.argv) > 2:
        message = sys.argv[2]
    else:
        if hasattr(sys.stdin, 'isatty') and not sys.stdin.isatty():
            try:
                message = sys.stdin.read().strip()
            except:
                pass

    print(f"→ 目标 / Target: {contact}")
    if message:
        print(f"→ 消息 / Message: {message}")

    if not ensure_wechat():
        sys.exit(1)

    # ===== 关键改动：先点击聊天标签，然后搜索并打开联系人 =====
    # Key change: click chat tab first, then search and open contact
    if not search_and_open(contact):
        print(f"失败：无法打开 {contact} / Failed to open {contact}")
        sys.exit(1)

    print("→ 已打开聊天 / Chat opened")

    if message:
        send_message(message)
        print(f"✓ 已发送 / Sent: {message}")
    else:
        print("✓ 已打开聊天页面 / Chat page opened")

    sys.exit(0)
