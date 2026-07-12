# 微信管家 / WeChat Butler

> AI 主动发消息 + 自动回复，**全部本地处理**，聊天内容不离机。
> Send messages on demand + auto-reply — **fully local**, no external API.

---

## 快速安装 / Quick Install

```powershell
# 右键 install.ps1 → 用 PowerShell 运行
# 所有依赖从 offline_pkgs/ 离线安装，无需联网
```

**安装完成后** 设置环境变量（使 PaddleX 跳过网络检测更快启动）：

```powershell
# install.ps1 已自动设置。如需手动：
[System.Environment]::SetEnvironmentVariable("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True", "User")
```

---

## 用法 / Usage

### 📨 发消息 / Send Message

```text
给 小明 发消息：中午一起去吃饭吗？
send Kitty: Want to grab lunch?
```

### 🤖 读聊天 + 回复 / Read Chat & Reply

```text
使用技能:reply-wechat-message 给：小明 回复
回复 小明
reply Kitty
```

### 回复模式 / Reply Modes

| 用户指令 | AI 行为 |
|----------|---------|
| "以后直接回不用问我" | 自动回复，不通知 |
| "回复前先问我" | 输出内容+建议，等用户确认 |
| （默认） | 输出内容+建议，问是否发送 |

详见 `RULES.md`。

---

## 目录结构 / Structure

```
reply-wechat-message/
├── SKILL.md                    # OpenClaw 技能定义
├── README.md                   # 本文件
├── RULES.md                    # 自动回复规则（AI必读）
├── THIRD_PARTY_LICENSES.md     # 第三方开源许可声明
├── LICENSE                     # 本技能许可证
├── install.ps1                 # 一键安装脚本
├── offline_pkgs/               # 离线 pip 包（~300MB）
│   ├── paddlepaddle-3.1.0-*.whl
│   ├── paddlex-3.7.2-*.whl
│   ├── numpy-*.whl
│   ├── Pillow-*.whl
│   ├── pyautogui-*.whl
│   ├── pygetwindow-*.whl
│   ├── pyperclip-*.whl
│   └── ... (所有传递依赖)
├── tessdata/                   # Tesseract 语言包（--v1 fallback用）
│   ├── chi_sim.traineddata
│   └── eng.traineddata
└── scripts/
    ├── send_wechat.py          # 发消息
    ├── reply_wechat.py         # 读上下文 + 回复
    └── open_wechat.py          # 启动/唤醒微信
```

---

## 技术栈 / Tech Stack

- **OCR**: PaddleX 3.7.2 + PaddleOCR（本地），Tesseract 5.5（fallback）
- **深度学习框架**: PaddlePaddle 3.1.0
- **GUI自动化**: pyautogui, pygetwindow, pyperclip
- **图像处理**: Pillow, numpy
- **截图方式**: Alt+PrtSc（绕过 BitBlt 截屏限制）

---

## 许可 / License

本技能本身基于 MIT 许可证开源。使用到的第三方开源软件详见 `THIRD_PARTY_LICENSES.md`。

MIT License — see `LICENSE` file for details.
