# 微信管家 / WeChat Butler

微信AI助手，无需复杂配置。只要电脑装了微信，说一声就能发消息和自动回复。
WeChat AI assistant — no complicated setup. Just install WeChat, then send messages and auto-reply by voice.

---

## 准备 / Prerequisites

- **Windows 电脑**，已安装微信并登录 / WeChat installed and logged in on Windows
- **微信固定在任务栏** / Pin WeChat to taskbar（点击任务栏微信图标能直接打开 / so clicking the taskbar icon opens it）
- **OpenClaw** 已安装并运行 / OpenClaw installed and running

---

## 安装 / Installation

**一键安装 / One-Click Install:**

```
解压 → 右键 install.ps1 → 用 PowerShell 运行
Extract → right-click install.ps1 → Run with PowerShell
```

安装脚本会自动 / The script will:
1. 复制技能文件到 `~/.openclaw/skills/reply-wechat-message`
2. 安装 Python 依赖（pyautogui, pygetwindow 等）
3. 重启 OpenClaw

---

## 使用 / Usage

### ① 主动发消息 / Send Message

**中文：** `给 [联系人] 发消息：[内容]`
**English:** `send [contact] [message]`

| 中文 | English |
|---|---|
| 给 小明 发消息：中午一起去吃饭吗？ | send Kitty: Want to grab lunch? |
| 发消息给 小红：记得带文件 | msg Peter: Don't forget the docs |
| 帮 小张 发消息：生日快乐！ | message Tom: Happy birthday! |

### ② 自动回复 / Auto-Reply

**中文：** `使用技能:reply-wechat-message 给：[联系人] 回复`
**English:** `reply [contact]`

| 中文 | English |
|---|---|
| 使用技能:reply-wechat-message 给：小明 回复 | reply Kitty |
| 回复 小红 | reply Peter |
| 回 小张 | reply Tom |

---

## 工作原理 / How It Works

1. **发消息** — AI 调用 `send_wechat.py`，自动打开微信、搜索联系人、粘贴发送
2. **自动回复** — 截图聊天窗口 → OCR 识别文字 → AI 分析上下文 → 自动生成回复并发送
3. 全部通过任务栏图标操控微信，无需任何插件或辅助软件
4. Everything runs via the WeChat taskbar icon — no plugins or extra software needed

---

## 注意事项 / Notes

- 使用前**微信必须在运行并登录** / WeChat **must be running and logged in**
- 微信必须**固定在任务栏**，脚本通过点击任务栏绿色图标唤醒 / WeChat must be **pinned to taskbar** — the script clicks the green icon to bring it up
- 首次使用可能需要微调搜索框点击位置（见 `SEARCH_X_REL` / `SEARCH_Y_REL`）
- 默认使用 OCR.space 免费 API（每天有额度），建议注册免费 Key 替换

---

## 开源 / Open Source

MIT License — 完全开源，随意使用和修改 / Fully open source, free to use and modify.
