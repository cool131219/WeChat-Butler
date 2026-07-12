# Third-Party Licenses / 第三方开源许可声明

本技能（微信管家 / WeChat Butler）使用了以下开源项目。根据各开源许可证的要求，在此列出其版权和许可信息。

This skill (WeChat Butler) uses the following open-source projects. Their copyright and license information are listed below as required.

---

## 核心依赖 / Core Dependencies

| Package | Version | License | Homepage |
|---------|---------|---------|----------|
| paddlepaddle | 3.1.0 | Apache-2.0 | https://github.com/PaddlePaddle/Paddle |
| paddlex | 3.7.2 | Apache-2.0 | https://github.com/PaddlePaddle/PaddleX |
| PaddleOCR (via paddlex) | - | Apache-2.0 | https://github.com/PaddlePaddle/PaddleOCR |
| pyautogui | latest | BSD-3-Clause | https://github.com/asweigart/pyautogui |
| pygetwindow | latest | BSD-3-Clause | https://github.com/asweigart/pygetwindow |
| pyperclip | latest | BSD-3-Clause | https://github.com/asweigart/pyperclip |
| Pillow | latest | Historical (HPND) | https://github.com/python-pillow/Pillow |
| numpy | latest | BSD-3-Clause | https://github.com/numpy/numpy |

## 间接依赖 / Transitive Dependencies

| Package | License | Notes |
|---------|---------|-------|
| aistudio-sdk | Apache-2.0 | 百度 AI Studio SDK |
| annotated-types | MIT | Python type annotations |
| anyio | MIT | Async I/O |
| bce-python-sdk | Apache-2.0 | 百度云 Python SDK |
| certifi | MPL-2.0 | SSL证书 |
| chardet | LGPL-2.1+ | 编码检测 |
| charset-normalizer | MIT | 字符编码标准化 |
| click | BSD-3-Clause | CLI工具 |
| colorama | BSD-3-Clause | 终端颜色 |
| colorlog | MIT | 日志着色 |
| crc32c | BSD-3-Clause / LGPL-2.1+ | CRC32C 校验 |
| decorator | BSD-2-Clause | 装饰器工具 |
| filelock | The Unlicense | 文件锁 |
| fsspec | BSD-3-Clause | 文件系统抽象 |
| future | MIT | Python 2/3 兼容 |
| h11 | MIT | HTTP/1.1 协议 |
| hf-xet | MIT | HuggingFace Xet |
| httpcore | BSD-3-Clause | HTTP 核心 |
| httpx | BSD-3-Clause | HTTP 客户端 |
| huggingface-hub | Apache-2.0 | HuggingFace Hub |
| idna | BSD-3-Clause | IDNA 国际化域名 |
| modelscope | Apache-2.0 | ModelScope 平台 |
| modelscope-hub | Apache-2.0 | ModelScope Hub |
| networkx | BSD-3-Clause | 图网络 |
| opt-einsum | MIT | 张量优化 |
| packaging | Apache-2.0 / BSD-2-Clause | 版本管理 |
| pandas | BSD-3-Clause | 数据分析 |
| prettytable | BSD-3-Clause | 表格美化 |
| protobuf | BSD-3-Clause | 序列化协议 |
| psutil | BSD-3-Clause | 系统进程工具 |
| py-cpuinfo | MIT | CPU 信息 |
| pycryptodome | BSD-2-Clause / Public Domain | 加密库 |
| pydantic | MIT | 数据校验 |
| pydantic-core | MIT | Pydantic 核心 |
| pymsgbox | BSD-3-Clause | 消息弹窗 |
| PyRect | BSD-3-Clause | 矩形运算 |
| PyScreeze | BSD-3-Clause | 屏幕坐标 |
| python-dateutil | Apache-2.0 / BSD-3-Clause | 日期处理 |
| pytweening | BSD-3-Clause | 动画插值 |
| PyYAML | MIT | YAML 解析 |
| requests | Apache-2.0 | HTTP 请求 |
| ruamel.yaml | MIT | YAML 处理 |
| setuptools | MIT | Python 包工具 |
| six | MIT | Python 2/3 兼容 |
| tqdm | MPL-2.0 / MIT | 进度条 |
| typing-extensions | Python-2.0 (PSF) | 类型注解 |
| typing-inspection | MIT | 类型检查 |
| tzdata | Apache-2.0 | 时区数据 |
| ujson | BSD-3-Clause | 快速 JSON |
| urllib3 | MIT | HTTP 客户端 |
| wcwidth | MIT | 字符宽度 |

## 附加工具 / Additional Tools

| Tool | License | Homepage |
|------|---------|----------|
| Tesseract OCR 5.5.0 | Apache-2.0 | https://github.com/tesseract-ocr/tesseract |

---

## 合规说明 / Compliance Notes

本技能遵循所有上游依赖的许可要求：
- **Apache-2.0 / BSD 系**：可自由使用、修改、分发，需保留版权声明
- **MIT / Unlicense**：可自由使用、修改、分发，无强制要求
- **LGPL-2.1+**（chardet）：动态链接使用，不影响本技能的许可证
- **MPL-2.0**（certifi, tqdm）：源码修改需公开，静态使用无需额外义务

如有任何遗漏或需要更详细的许可信息，请联系项目维护者。
If any attribution is missing or you need more detailed license information, please contact the project maintainer.
