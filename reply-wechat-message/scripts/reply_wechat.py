"""
回复微信联系人 — 读取当前页面全部聊天上下文，区分说话人
用法:
  python reply_wechat.py <联系人>               # 只读上下文
  echo "回复" | python reply_wechat.py <联系人>  # 读上下文 + 发送回复

输出:
  ★上下文开始★
  [对方] xxx
  [我] xxx
  ★上下文结束★

AI 注意: 输出中包含系统提示(灰色小字如撤回消息、时间戳等)和真实对话，请自行区分
"""
import pyautogui, pygetwindow as gw, time, pyperclip, os, subprocess, sys, base64, io, requests
from PIL import Image
import numpy as np
import mss

pyautogui.FAILSAFE = False

SEARCH_X_REL = 90
SEARCH_Y_REL = 73

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
OPEN_SCRIPT = os.path.join(SCRIPTS_DIR, 'open_wechat.py')
SEND_SCRIPT = os.path.join(SCRIPTS_DIR, 'send_wechat.py')
PYTHON = 'python'


def ensure_wechat():
    """确保微信在前台（无截图fallback，桌面不可用时也不崩溃）"""
    wins = gw.getWindowsWithTitle('微信')
    if not wins:
        print("→ 微信未运行，启动中...")
        if os.path.exists(OPEN_SCRIPT):
            subprocess.run([PYTHON, OPEN_SCRIPT], capture_output=True, text=True, timeout=60)
            time.sleep(2)
        else:
            print("错误: 找不到 open_wechat.py", file=sys.stderr)
            return False
        wins = gw.getWindowsWithTitle('微信')
        if not wins:
            return False
    w = wins[0]
    if w.isMinimized:
        w.restore()
        time.sleep(0.5)
    try:
        w.activate()
    except:
        pass
    time.sleep(1)

    # 使用Win32 API SetForegroundWindow 更可靠
    try:
        import ctypes
        user32 = ctypes.windll.user32
        hwnd = w._hWnd
        user32.SetForegroundWindow(hwnd)
        time.sleep(0.3)
    except:
        pass

    return True


def click_chat_tab():
    """点击侧边聊天图标，确保在聊天页面"""
    for _ in range(5):
        wins = gw.getWindowsWithTitle('微信')
        if not wins:
            continue
        w = wins[0]
        pyautogui.click(w.left + 41, w.top + 130)
        time.sleep(0.3)


def search_and_open(name):
    """点击聊天标签 → 搜索联系人 → 打开聊天"""
    click_chat_tab()
    time.sleep(0.5)

    wins = gw.getWindowsWithTitle('微信')
    if not wins:
        return None
    w = wins[0]
    left, top = w.left, w.top

    pyautogui.moveTo(left + 60 + SEARCH_X_REL, top + SEARCH_Y_REL, duration=0.05)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    time.sleep(0.3)

    pyperclip.copy(name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    pyautogui.press('enter')
    time.sleep(2)

    return gw.getWindowsWithTitle('微信')[0] if gw.getWindowsWithTitle('微信') else None


def ocr_image(img):
    """OCR.space 识图"""
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode()

    for retry in range(2):
        try:
            r = requests.post(
                'https://api.ocr.space/parse/image',
                data={
                    'base64Image': f'data:image/png;base64,{b64}',
                    'language': 'chs',
                    'OCREngine': '2',
                    'scale': 'true'
                },
                headers={'apikey': 'helloworld'},
                timeout=30
            )
            data = r.json()
            if data.get('ParsedResults'):
                text = data['ParsedResults'][0]['ParsedText'].strip()
                if text:
                    return text
        except Exception as e:
            if retry == 1:
                print(f"OCR错误: {e}", file=sys.stderr)
    return ""


def read_chat_context():
    """截图聊天消息区 → OCR → 输出全文（Alt+PrtSc绕过BitBlt）"""
    wins = gw.getWindowsWithTitle('微信')
    if not wins:
        return ""
    w = wins[0]
    left, top, ww, wh = w.left, w.top, w.width, w.height

    # 确保微信在前台（Alt+PrtSc只截活动窗口）
    if w.isMinimized:
        w.restore()
    try: w.activate()
    except: pass
    try:
        import ctypes
        ctypes.windll.user32.SetForegroundWindow(w._hWnd)
    except: pass
    time.sleep(0.5)

    # Alt+PrtSc 截图当前活动窗口（绕过BitBlt限制）
    pyautogui.hotkey('alt', 'printscreen')
    time.sleep(0.5)

    from PIL import ImageGrab
    full = ImageGrab.grabclipboard()
    if not full or not isinstance(full, Image.Image):
        print("  Alt+PrtSc 截图失败", file=sys.stderr)
        return ""

    print(f"  Alt+PrtSc 截图: {full.size}", file=sys.stderr)

    # 裁剪出聊天消息区
    crop_left = 250
    crop_right = full.width - 10
    crop_top = 55
    crop_bottom = full.height - 85
    cw = crop_right - crop_left
    ch = crop_bottom - crop_top
    if cw <= 0 or ch <= 0:
        return ""

    chat = full.crop((crop_left, crop_top, crop_right, crop_bottom))

    # 放大2x提高OCR识别率
    big = chat.resize((cw * 2, ch * 2), Image.LANCZOS)

    # 保存调试截图
    debug_dir = os.path.join(os.path.expanduser('~'), 'Pictures', 'OpenClaw')
    os.makedirs(debug_dir, exist_ok=True)
    big.save(os.path.join(debug_dir, 'chat_full.png'))

    # OCR
    print("  → OCR...", file=sys.stderr)
    text = ocr_image(big)
    print(f"  共{len(text) if text else 0}字符", file=sys.stderr)

    lines = ["★上下文开始★",
             "# AI注意: 以下是OCR读取的聊天区域全貌",
             "# 白底气泡=对方发的消息，绿底气泡=自己发的消息"]
    if text:
        for l in text.split('\n'):
            if l.strip():
                lines.append(l.strip())
    else:
        lines.append("(未读取到聊天内容)")
    lines.append("★上下文结束★")
    return '\n'.join(lines)


def send_reply(contact, message):
    """调用 send_wechat.py 发送消息"""
    if not os.path.exists(SEND_SCRIPT):
        print("错误: 找不到 send_wechat.py", file=sys.stderr)
        return False
    result = subprocess.run(
        [PYTHON, SEND_SCRIPT, contact],
        input=message,
        capture_output=True,
        text=True,
        timeout=30
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"发送错误: {result.stderr}", file=sys.stderr)
        return False
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python reply_wechat.py <联系人>", file=sys.stderr)
        print("  echo '消息' | python reply_wechat.py <联系人>", file=sys.stderr)
        sys.exit(1)

    contact = sys.argv[1]

    reply_msg = None
    if hasattr(sys.stdin, 'isatty') and not sys.stdin.isatty():
        try:
            reply_msg = sys.stdin.read().strip()
        except:
            pass

    if not ensure_wechat():
        print("微信无法打开", file=sys.stderr)
        sys.exit(1)

    w = search_and_open(contact)
    if not w:
        print(f"无法打开 {contact}", file=sys.stderr)
        sys.exit(1)

    time.sleep(0.5)
    context = read_chat_context()

    if reply_msg:
        print(f"→ 发送回复: {reply_msg[:50]}...")
        send_reply(contact, reply_msg)

    if context:
        print(context)
    else:
        print("★上下文开始★")
        print("(未读取到聊天内容)")
        print("★上下文结束★")

    sys.exit(0)
