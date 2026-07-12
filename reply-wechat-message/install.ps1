# reply-wechat-message 一键安装脚本
# 使用方法：右键 → 用 PowerShell 运行
#
# 本脚本从离线包目录 offline_pkgs/ 安装所有依赖
# 不需要联网下载 Python 包

Write-Host "===== reply-wechat-message 安装开始 =====" -ForegroundColor Cyan

$skillName = "reply-wechat-message"
$sourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetDir = "$env:USERPROFILE\.openclaw\skills\$skillName"

# 1. 复制技能文件
Write-Host "[1/5] 复制技能文件..." -ForegroundColor Yellow
if (-not (Test-Path "$env:USERPROFILE\.openclaw\skills")) {
    New-Item -ItemType Directory -Path "$env:USERPROFILE\.openclaw\skills" -Force | Out-Null
}
if (Test-Path $targetDir) {
    Remove-Item -Recurse -Force $targetDir
}
Copy-Item -Recurse -Force "$sourceDir\..\$skillName" $targetDir
Write-Host "      ✓ 已复制到 $targetDir" -ForegroundColor Green

# 2. 从离线包安装 Python 依赖
Write-Host "[2/5] 从离线包安装 Python 依赖..." -ForegroundColor Yellow
$offlineDir = "$targetDir\offline_pkgs"
if (Test-Path $offlineDir) {
    $pkgCount = (Get-ChildItem $offlineDir -Filter "*.whl" | Measure-Object).Count
    $tarCount = (Get-ChildItem $offlineDir -Filter "*.tar.gz" | Measure-Object).Count
    Write-Host "      发现 $pkgCount 个 whl 包 + $tarCount 个 tar.gz 源包" -ForegroundColor White
    
    # 先安装核心依赖（顺序敏感）
    $corePkgs = @("numpy", "Pillow", "pyautogui", "pygetwindow", "pyperclip")
    foreach ($pkg in $corePkgs) {
        pip install --no-index --find-links $offlineDir $pkg 2>&1 | Out-Null
    }
    Write-Host "      ✓ 核心依赖安装完成" -ForegroundColor Green
    
    # 安装 PaddlePaddle 和 PaddleX（大包，可能需要点时间）
    Write-Host "      正在安装 PaddlePaddle 3.1.0 (~100MB)..."
    pip install --no-index --find-links $offlineDir paddlepaddle==3.1.0 2>&1 | Out-Null
    Write-Host "      ✓ PaddlePaddle 安装完成" -ForegroundColor Green
    
    Write-Host "      正在安装 PaddleX 3.7.2..."
    pip install --no-index --find-links $offlineDir paddlex 2>&1 | Out-Null
    Write-Host "      ✓ PaddleX 安装完成" -ForegroundColor Green
} else {
    Write-Host "      ⚠ 未找到离线包目录，联网安装..." -ForegroundColor Yellow
    pip install pyautogui pygetwindow pyperclip Pillow numpy paddlepaddle==3.1.0 paddlex -q
}

Write-Host "      ✓ Python 依赖安装完成" -ForegroundColor Green

# 2.5 复制 PaddleX 离线模型到缓存目录（首次安装时预置，后续无需联网下载）
Write-Host "[2.5/5] 复制 PaddleX 离线模型到缓存..." -ForegroundColor Yellow
$modelSrc = "$targetDir\paddlex_models"
$modelDst = "$env:USERPROFILE\.paddlex\official_models"
if (Test-Path $modelSrc) {
    New-Item -ItemType Directory -Path $modelDst -Force | Out-Null
    Get-ChildItem $modelSrc -Directory | ForEach-Object {
        $dstPath = Join-Path $modelDst $_.Name
        if (-not (Test-Path $dstPath)) {
            Write-Host "      复制模型: $($_.Name)..." -ForegroundColor White
            Copy-Item -Recurse $_.FullName $dstPath
        } else {
            Write-Host "      模型已存在: $($_.Name)" -ForegroundColor DarkGray
        }
    }
    Write-Host "      ✓ PaddleX 离线模型已缓存（~185MB）" -ForegroundColor Green
} else {
    Write-Host "      ⚠ 未找到离线模型包，首次运行时会联网下载" -ForegroundColor Yellow
}

# 3. 设置环境变量（跳过 PaddleX 网络检测）
Write-Host "[3/5] 配置环境变量..." -ForegroundColor Yellow
$currentUser = [System.EnvironmentVariableTarget]::User
[System.Environment]::SetEnvironmentVariable("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True", $currentUser)
Write-Host "      ✓ 已设置 PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True" -ForegroundColor Green

# 4. 检查 Tesseract OCR（--v1 模式需要用）
Write-Host "[4/5] 检查 Tesseract OCR（--v1 模式需要）..." -ForegroundColor Yellow
$tessCandidates = @(
    "C:\Program Files\Tesseract-OCR\tesseract.exe",
    "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    "$env:USERPROFILE\Tesseract-OCR\tesseract.exe"
)
$foundTess = $false
foreach ($p in $tessCandidates) {
    if (Test-Path $p) {
        Write-Host "      ✓ 已找到: $p" -ForegroundColor Green
        $foundTess = $true
        break
    }
}
if (-not $foundTess) {
    Write-Host "      ⚠ 未找到 Tesseract（可选，仅 --v1 模式需要）" -ForegroundColor Yellow
    Write-Host "      需要时请从 https://github.com/UB-Mannheim/tesseract/wiki 下载" -ForegroundColor White
}

# 5. 重启 OpenClaw
Write-Host "[5/5] 重启 OpenClaw..." -ForegroundColor Yellow
openclaw gateway restart
Write-Host "      ✓ 已触发重启" -ForegroundColor Green

Write-Host ""
Write-Host "===== 安装完成 =====" -ForegroundColor Cyan
Write-Host "安装后 OpenClaw 会自动重启并加载新技能。" -ForegroundColor Cyan
Write-Host "使用方式：在对话中输入" -ForegroundColor White
Write-Host '  使用技能:reply-wechat-message 给：[联系人] 回复' -ForegroundColor Magenta
Write-Host "技能功能：读取聊天上下文 → AI分析 → 自动/手动回复" -ForegroundColor White
Write-Host ""
Write-Host "第三方开源许可声明见：THIRD_PARTY_LICENSES.md" -ForegroundColor White
