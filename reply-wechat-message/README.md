# 微信管家 / WeChat Butler

> AI 主动发消息 + 自动回复，解放你的微信。
> Send messages on demand + auto-reply — liberate your WeChat.

自包含的 OpenClaw 技能包，无需额外安装其他依赖。
A self-contained OpenClaw skill for the OpenClaw agent platform — no external setup required.

---

## 这是什么？/ What Is This?

微信管家是一个 OpenClaw 技能，让你的 AI 助手能操控微信：
- **主动发消息** — 告诉 AI "给小明发消息说中午一起吃饭"，AI 自动打开微信搜索联系人并发送
- **自动回复** — AI 读取微信聊天窗口的截图，通过 OCR 识别对话内容，分析后自动生成回复并发送

WeChat Butler is an OpenClaw skill that gives your AI agent the ability to control WeChat:
- **Send messages** — Tell AI "send Kitty a message saying let's have lunch", and it opens WeChat, finds the contact, and sends
- **Auto-reply** — AI screenshots the chat window, OCRs the conversation, analyzes the context, and replies automatically

---

## 功能 / Features

### 📨 主动发消息 / Send Message

直接告诉 AI 给谁发什么，自动完成。
Just tell the AI who to message and what to say — it handles the rest.

**触发格式 / Trigger Format:**

**中文 / Chinese:**
```
给 [联系人] 发消息：[内容]
发消息给 [联系人]：[内容]
帮 [联系人] 发消息：[内容]
```

**English:**
```
send [contact] [message]
msg [contact] [message]
message [contact] [message]
```

**示例 / Examples:**

| 中文 / Chinese | English |
|---|---|
| `给 小明 发消息：中午一起去吃饭吗？` | `send Kitty: Want to grab lunch?` |
| `发消息给 小红：记得带文件` | `msg Peter: Don't forget the documents` |
| `帮 小张 发消息：生日快乐！` | `message Tom: Happy birthday!` |

**执行流程 / Execution Flow:**
1. AI 提取联系人和消息内容 / AI extracts contact name and message content
2. `python scripts/send_wechat.py <联系人> <消息>` — 打开微信 → 搜索联系人 → 打开聊天 → 粘贴发送
3. 返回发送结果给用户 / Report result to user

---

### 🤖 AI 自动回复 / Auto-Reply

读取聊天上下文，AI 分析后自动回复。
Reads the entire chat context, AI analyzes and auto-replies.

**触发格式 / Trigger Format:**
```
使用技能:reply-wechat-message 给：[联系人] 回复
```

**示例 / Examples:**
| 中文 / Chinese | English |
|---|---|
| `使用技能:reply-wechat-message 给：小明 回复` | `使用技能:reply-wechat-message 给：Kitty 回复` |
| `回复 小红` | `reply Peter` |
| `回 小张` | `回 Tom` |

**执行流程 / Execution Flow:**
1. `python scripts/reply_wechat.py <联系人>` — 截图聊天窗口 → OCR 识别对话 → 输出结构化上下文
2. AI 分析全部上下文，理解对话脉络，生成合适的回复 / AI analyzes full context and generates a reply
3. `echo "回复" | python scripts/reply_wechat.py <联系人>` — 读取上下文 + 自动发送（一步完成）

**输出格式 / Output Format:**
```
★上下文开始★ / ★Context Start★
[对方/Them] 你吃饭了吗
[我/Me] 吃过了，你呢
★上下文结束★ / ★Context End★
```

---

### 🔍 OCR 识图 / OCR Recognition

- 通过 Alt+PrtSc 截取微信窗口，绕过 BitBlt 截屏限制
- 从 Clipboard 读取截图，裁剪出聊天消息区域
- 调用 OCR.space API（免费版）进行中英文 OCR 识别
- 自动区分左右气泡：左侧白底 = 对方消息，右侧绿底 = 自己消息

- Uses Alt+PrtSc to capture the WeChat window (bypasses BitBlt restrictions)
- Reads from clipboard, crops the chat message area
- Uses OCR.space API (free tier) for Chinese/English OCR
- Automatically distinguishes left (other party) vs right (self) messages

---

## 安装 / Installation

```bash
# 简单：解压后右键 install.ps1 → 用 PowerShell 运行
# Easy: Extract, right-click install.ps1 → Run with PowerShell
```

安装脚本会自动 / The install script will:
1. 复制技能文件到 `~/.openclaw/skills/reply-wechat-message` / Copy skill files
2. 安装 Python 依赖 / Install Python packages: `pyautogui, pygetwindow, pyperclip, requests, Pillow, numpy`
3. 重启 OpenClaw / Restart OpenClaw

### 手动配置 / Manual Configuration

详见 `INSTALL.md` 或以下摘要 / See `INSTALL.md` for details:

| 配置项 / Item | 说明 / Note |
|---|---|
| Python 路径 / Python Path | 如 `python` 不是目标版本，改 `scripts/reply_wechat.py` 中的 `PYTHON='python'` |
| OCR Key | `scripts/reply_wechat.py` 中 `helloworld` 是演示 Key，建议 https://ocr.space 注册免费 Key |
| 搜索框位置 / Search Position | `SEARCH_X_REL` / `SEARCH_Y_REL` 可微调点击位置 |

---

## 目录结构 / Project Structure

```
reply-wechat-message/
├── README.md           # 本文件 / This file
├── SKILL.md            # OpenClaw 技能定义 / Skill definition for OpenClaw
├── INSTALL.md          # 详细安装指南 / Detailed installation guide
├── install.ps1         # 一键安装 PowerShell 脚本 / One-click install script
└── scripts/
    ├── send_wechat.py      # 发消息脚本（搜索联系人 + 发送）/ Send message script
    ├── reply_wechat.py     # 主脚本（读取上下文 + 发送回复）/ Main script: read context & reply
    └── open_wechat.py      # 启动微信脚本（点击任务栏图标）/ Launch WeChat via taskbar icon
```

## 隐私说明 / Privacy Note

- 所有脚本**不包含任何个人信息**（无用户名、目录、真实联系人）
- OCR 通过 OCR.space API 在云端处理，仅发送聊天截图
- 所有操作在本地 Windows 上执行，AI 通过命令行调用脚本

- All scripts are **free of personal information** (no usernames, paths, or real contacts)
- OCR is processed via OCR.space API — only chat screenshots are sent
- All operations run locally on Windows; AI invokes scripts via command line

---

## 许可 / License

MIT
