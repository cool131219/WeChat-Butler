# reply-wechat-message 一键安装脚本
# 使用方法：右键 → 用 PowerShell 运行

Write-Host "===== reply-wechat-message 安装开始 =====" -ForegroundColor Cyan

$skillName = "reply-wechat-message"
$sourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetDir = "$env:USERPROFILE\.openclaw\skills\$skillName"

# 1. 复制技能文件
Write-Host "[1/4] 复制技能文件..." -ForegroundColor Yellow
if (-not (Test-Path "$env:USERPROFILE\.openclaw\skills")) {
    New-Item -ItemType Directory -Path "$env:USERPROFILE\.openclaw\skills" -Force | Out-Null
}
if (Test-Path $targetDir) {
    Remove-Item -Recurse -Force $targetDir
}
Copy-Item -Recurse -Force "$sourceDir\..\$skillName" $targetDir
Write-Host "      ✓ 已复制到 $targetDir" -ForegroundColor Green

# 2. 安装 Python 依赖
Write-Host "[2/4] 安装 Python 依赖..." -ForegroundColor Yellow
$deps = @("pyautogui", "pygetwindow", "pyperclip", "requests", "Pillow", "numpy")
foreach ($dep in $deps) {
    pip install $dep -q
}
Write-Host "      ✓ Python 依赖安装完成" -ForegroundColor Green

# 3. 提醒 OCR.space 配置
Write-Host "[3/4] OCR.space API Key" -ForegroundColor Yellow
Write-Host "      脚本依赖 OCR.space 免费版做文字识别。" -ForegroundColor White
Write-Host "      请打开 scripts\reply_wechat.py，找到 api_key 变量，填入你的 Key。" -ForegroundColor White
Write-Host "      注册地址：https://ocr.space" -ForegroundColor White

# 4. 重启 OpenClaw
Write-Host "[4/4] 重启 OpenClaw..." -ForegroundColor Yellow
openclaw gateway restart
Write-Host "      ✓ 已触发重启" -ForegroundColor Green

Write-Host ""
Write-Host "===== 安装完成 =====" -ForegroundColor Cyan
Write-Host "安装后 OpenClaw 会自动重启并加载新技能。" -ForegroundColor Cyan
Write-Host "使用方式：在对话中输入" -ForegroundColor White
Write-Host '  使用技能:reply-wechat-message 给：[联系人] 回复' -ForegroundColor Magenta
Write-Host "技能功能：读取聊天上下文 → AI分析 → 自动发送回复" -ForegroundColor White
