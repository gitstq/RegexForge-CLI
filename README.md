<!-- 
  RegexForge-CLI README
  Multi-language support: 简体中文 | 繁體中文 | English
-->

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/dependencies-0-brightgreen.svg" alt="Dependencies">
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> | 
  <a href="#繁體中文">繁體中文</a> | 
  <a href="#english">English</a>
</p>

---

<a name="简体中文"></a>
## 🎉 项目介绍

**RegexForge-CLI** 是一款**轻量级终端正则表达式测试与构建引擎**，专为开发者打造。零外部依赖，纯Python标准库实现，让您在终端中高效测试、调试和构建正则表达式。

### 🎯 解决的痛点
- ❌ 每次测试正则都要打开浏览器访问在线工具
- ❌ 无法快速验证正则表达式的匹配结果
- ❌ 需要手动编写多语言的正则代码
- ❌ 缺少常用正则模式的快速参考

### ✨ 自研差异化亮点
- 🚀 **零依赖** - 仅使用Python标准库，开箱即用
- 🎨 **TUI交互界面** - 美观的终端图形界面，实时测试
- 📚 **50+内置模板** - 涵盖邮箱、手机、URL、IP等常用模式
- 💻 **8种语言代码生成** - Python/JS/Go/Rust/Java/PHP/Ruby/TypeScript
- ⚡ **实时高亮** - 匹配结果彩色高亮显示
- 📊 **性能分析** - 显示匹配耗时，优化正则性能
- 💾 **历史记录** - 本地保存测试历史，随时回溯

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔍 **实时匹配测试** | 输入正则和文本，即时显示匹配结果 |
| 🎨 **语法高亮** | 匹配部分彩色高亮，一目了然 |
| 📦 **捕获分组** | 可视化显示所有捕获组内容 |
| 🚀 **代码生成** | 自动生成多语言代码片段 |
| 📚 **模板库** | 50+常用正则表达式模板 |
| 🔧 **标志管理** | 支持所有re模块标志 |
| 💾 **历史记录** | 本地保存测试历史 |
| 📊 **性能分析** | 显示匹配耗时 |

---

## 🚀 快速开始

### 📋 环境要求
- Python 3.8 或更高版本
- 无需安装任何外部依赖

### 📥 安装方式

**方式一：从源码安装**
```bash
# 克隆仓库
git clone https://github.com/gitstq/RegexForge-CLI.git
cd RegexForge-CLI

# 安装
pip install -e .
```

**方式二：直接运行**
```bash
# 克隆仓库
git clone https://github.com/gitstq/RegexForge-CLI.git
cd RegexForge-CLI

# 直接运行
python -m regexforge
```

### 🎮 启动方式

```bash
# 启动交互式TUI界面
regexforge

# 或使用Python模块方式
python -m regexforge
```

---

## 📖 详细使用指南

### 🔧 命令行模式

#### 1️⃣ 测试正则模式是否有效
```bash
regexforge test "^\d+$"
# ✓ Pattern is valid: ^\d+$
```

#### 2️⃣ 匹配文本开头
```bash
regexforge match "hello" "hello world"
# ✓ Match found!
#   Matched: hello
#   Position: 0-5
```

#### 3️⃣ 查找所有匹配
```bash
regexforge find "\d+" "a1b2c3d4"
# ✓ Found 4 match(es)
#   Text:
#     a[1]b[2]c[3]d[4]
```

#### 4️⃣ 生成多语言代码
```bash
# 生成Python代码
regexforge generate "^\w+$" -l python

# 生成JavaScript代码
regexforge generate "^\w+$" -l javascript

# 生成Go代码
regexforge generate "^\w+$" -l go
```

#### 5️⃣ 浏览模板库
```bash
# 列出所有模板
regexforge library

# 搜索邮箱相关模板
regexforge library email

# 按类别筛选
regexforge library -c "Email"
```

### 🖥️ TUI交互模式

启动TUI后，您可以使用以下快捷键：

| 快捷键 | 功能 |
|--------|------|
| `Tab` | 切换输入框（模式/文本） |
| `Enter` | 执行测试 |
| `L` | 打开模板库 |
| `G` | 打开代码生成 |
| `F` | 切换标志 |
| `Q` | 退出程序 |
| `Esc` | 返回主界面 |

### 🚩 支持的标志

| 标志 | 简写 | 描述 |
|------|------|------|
| `IGNORECASE` | `i` | 忽略大小写 |
| `MULTILINE` | `m` | 多行模式 |
| `DOTALL` | `s` | .匹配换行符 |
| `VERBOSE` | `x` | 详细模式 |
| `ASCII` | `a` | 仅ASCII匹配 |
| `UNICODE` | `u` | Unicode匹配 |

---

## 💡 设计思路与迭代规划

### 🏗️ 设计理念
RegexForge-CLI 的设计遵循以下原则：
1. **零依赖优先** - 使用Python标准库，确保最大兼容性
2. **终端原生** - 专为终端用户设计，无需离开命令行
3. **即时反馈** - 实时显示匹配结果，提高开发效率

### 📅 迭代规划
- [ ] **v1.1** - 添加正则表达式解释功能
- [ ] **v1.2** - 支持正则表达式性能优化建议
- [ ] **v1.3** - 添加正则表达式可视化功能
- [ ] **v1.4** - 支持批量测试文件

---

## 📦 打包与部署指南

### 本地开发
```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 代码格式化
black regexforge/
```

### 构建发布包
```bash
# 构建
python -m build

# 发布到PyPI
twine upload dist/*
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: 添加某个特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 提交规范
- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关

---

## 📄 开源协议说明

本项目采用 **MIT License** 开源协议。

```
MIT License

Copyright (c) 2025 RegexForge Team

Permission is hereby granted, free of charge...
```

详见 [LICENSE](LICENSE) 文件。

---

<p align="center">
  Made with ❤️ by RegexForge Team
</p>

---
---

<a name="繁體中文"></a>
## 🎉 專案介紹

**RegexForge-CLI** 是一款**輕量級終端正則表達式測試與構建引擎**，專為開發者打造。零外部依賴，純Python標準庫實現，讓您在終端中高效測試、調試和構建正則表達式。

### 🎯 解決的痛點
- ❌ 每次測試正則都要打開瀏覽器訪問線上工具
- ❌ 無法快速驗證正則表達式的匹配結果
- ❌ 需要手動編寫多語言的正則代碼
- ❌ 缺少常用正則模式的快速參考

### ✨ 自研差異化亮點
- 🚀 **零依賴** - 僅使用Python標準庫，開箱即用
- 🎨 **TUI互動介面** - 美觀的終端圖形介面，即時測試
- 📚 **50+內建模板** - 涵蓋郵箱、手機、URL、IP等常用模式
- 💻 **8種語言代碼生成** - Python/JS/Go/Rust/Java/PHP/Ruby/TypeScript
- ⚡ **即時高亮** - 匹配結果彩色高亮顯示
- 📊 **效能分析** - 顯示匹配耗時，優化正則效能
- 💾 **歷史記錄** - 本地保存測試歷史，隨時回溯

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔍 **即時匹配測試** | 輸入正則和文字，即時顯示匹配結果 |
| 🎨 **語法高亮** | 匹配部分彩色高亮，一目瞭然 |
| 📦 **捕獲分組** | 視覺化顯示所有捕獲組內容 |
| 🚀 **代碼生成** | 自動生成多語言代碼片段 |
| 📚 **模板庫** | 50+常用正則表達式模板 |
| 🔧 **標誌管理** | 支援所有re模組標誌 |
| 💾 **歷史記錄** | 本地保存測試歷史 |
| 📊 **效能分析** | 顯示匹配耗時 |

---

## 🚀 快速開始

### 📋 環境要求
- Python 3.8 或更高版本
- 無需安裝任何外部依賴

### 📥 安裝方式

**方式一：從原始碼安裝**
```bash
# 複製倉庫
git clone https://github.com/gitstq/RegexForge-CLI.git
cd RegexForge-CLI

# 安裝
pip install -e .
```

**方式二：直接執行**
```bash
# 複製倉庫
git clone https://github.com/gitstq/RegexForge-CLI.git
cd RegexForge-CLI

# 直接執行
python -m regexforge
```

### 🎮 啟動方式

```bash
# 啟動互動式TUI介面
regexforge

# 或使用Python模組方式
python -m regexforge
```

---

## 📖 詳細使用指南

### 🔧 命令列模式

#### 1️⃣ 測試正則模式是否有效
```bash
regexforge test "^\d+$"
# ✓ Pattern is valid: ^\d+$
```

#### 2️⃣ 匹配文字開頭
```bash
regexforge match "hello" "hello world"
# ✓ Match found!
#   Matched: hello
#   Position: 0-5
```

#### 3️⃣ 查找所有匹配
```bash
regexforge find "\d+" "a1b2c3d4"
# ✓ Found 4 match(es)
#   Text:
#     a[1]b[2]c[3]d[4]
```

#### 4️⃣ 生成多語言代碼
```bash
# 生成Python代碼
regexforge generate "^\w+$" -l python

# 生成JavaScript代碼
regexforge generate "^\w+$" -l javascript

# 生成Go代碼
regexforge generate "^\w+$" -l go
```

#### 5️⃣ 瀏覽模板庫
```bash
# 列出所有模板
regexforge library

# 搜尋郵箱相關模板
regexforge library email

# 按類別篩選
regexforge library -c "Email"
```

### 🖥️ TUI互動模式

啟動TUI後，您可以使用以下快速鍵：

| 快速鍵 | 功能 |
|--------|------|
| `Tab` | 切換輸入框（模式/文字） |
| `Enter` | 執行測試 |
| `L` | 開啟模板庫 |
| `G` | 開啟代碼生成 |
| `F` | 切換標誌 |
| `Q` | 退出程式 |
| `Esc` | 返回主介面 |

---

## 💡 設計思路與迭代規劃

### 🏗️ 設計理念
RegexForge-CLI 的設計遵循以下原則：
1. **零依賴優先** - 使用Python標準庫，確保最大相容性
2. **終端原生** - 專為終端使用者設計，無需離開命令列
3. **即時回饋** - 即時顯示匹配結果，提高開發效率

### 📅 迭代規劃
- [ ] **v1.1** - 添加正則表達式解釋功能
- [ ] **v1.2** - 支援正則表達式效能優化建議
- [ ] **v1.3** - 添加正則表達式視覺化功能
- [ ] **v1.4** - 支援批次測試檔案

---

## 📦 打包與部署指南

### 本地開發
```bash
# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest tests/

# 代碼格式化
black regexforge/
```

### 構建發布包
```bash
# 構建
python -m build

# 發布到PyPI
twine upload dist/*
```

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！

### 如何貢獻
1. Fork 本倉庫
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'feat: 添加某個特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 建立 Pull Request

---

## 📄 開源協議說明

本專案採用 **MIT License** 開源協議。

詳見 [LICENSE](LICENSE) 檔案。

---

<p align="center">
  Made with ❤️ by RegexForge Team
</p>

---
---

<a name="english"></a>
## 🎉 Introduction

**RegexForge-CLI** is a **lightweight terminal regex testing and building engine** designed for developers. Zero external dependencies, pure Python standard library implementation, allowing you to efficiently test, debug, and build regular expressions in the terminal.

### 🎯 Problems Solved
- ❌ Opening browser for online regex tools every time
- ❌ Unable to quickly verify regex match results
- ❌ Manually writing regex code in multiple languages
- ❌ Lack of quick reference for common regex patterns

### ✨ Key Highlights
- 🚀 **Zero Dependencies** - Uses only Python standard library, works out of the box
- 🎨 **TUI Interface** - Beautiful terminal GUI for real-time testing
- 📚 **50+ Built-in Templates** - Covers email, phone, URL, IP and more
- 💻 **8 Language Code Generation** - Python/JS/Go/Rust/Java/PHP/Ruby/TypeScript
- ⚡ **Real-time Highlighting** - Colorful match result highlighting
- 📊 **Performance Analysis** - Shows matching time for optimization
- 💾 **History Tracking** - Local storage of test history

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **Real-time Matching** | Input regex and text, instant match results |
| 🎨 **Syntax Highlighting** | Colorful match highlighting at a glance |
| 📦 **Capture Groups** | Visual display of all capture groups |
| 🚀 **Code Generation** | Auto-generate multi-language code snippets |
| 📚 **Pattern Library** | 50+ common regex patterns |
| 🔧 **Flag Management** | Support all re module flags |
| 💾 **History** | Local test history storage |
| 📊 **Performance** | Display matching time |

---

## 🚀 Quick Start

### 📋 Requirements
- Python 3.8 or higher
- No external dependencies required

### 📥 Installation

**Option 1: Install from Source**
```bash
# Clone repository
git clone https://github.com/gitstq/RegexForge-CLI.git
cd RegexForge-CLI

# Install
pip install -e .
```

**Option 2: Run Directly**
```bash
# Clone repository
git clone https://github.com/gitstq/RegexForge-CLI.git
cd RegexForge-CLI

# Run directly
python -m regexforge
```

### 🎮 Launch

```bash
# Launch interactive TUI
regexforge

# Or using Python module
python -m regexforge
```

---

## 📖 Detailed Usage Guide

### 🔧 Command Line Mode

#### 1️⃣ Test if pattern is valid
```bash
regexforge test "^\d+$"
# ✓ Pattern is valid: ^\d+$
```

#### 2️⃣ Match at text beginning
```bash
regexforge match "hello" "hello world"
# ✓ Match found!
#   Matched: hello
#   Position: 0-5
```

#### 3️⃣ Find all matches
```bash
regexforge find "\d+" "a1b2c3d4"
# ✓ Found 4 match(es)
#   Text:
#     a[1]b[2]c[3]d[4]
```

#### 4️⃣ Generate multi-language code
```bash
# Generate Python code
regexforge generate "^\w+$" -l python

# Generate JavaScript code
regexforge generate "^\w+$" -l javascript

# Generate Go code
regexforge generate "^\w+$" -l go
```

#### 5️⃣ Browse pattern library
```bash
# List all patterns
regexforge library

# Search email patterns
regexforge library email

# Filter by category
regexforge library -c "Email"
```

### 🖥️ TUI Interactive Mode

After launching TUI, use these keyboard shortcuts:

| Key | Function |
|-----|----------|
| `Tab` | Switch input field (pattern/text) |
| `Enter` | Execute test |
| `L` | Open pattern library |
| `G` | Open code generation |
| `F` | Toggle flags |
| `Q` | Quit program |
| `Esc` | Return to main screen |

### 🚩 Supported Flags

| Flag | Short | Description |
|------|-------|-------------|
| `IGNORECASE` | `i` | Case-insensitive |
| `MULTILINE` | `m` | Multiline mode |
| `DOTALL` | `s` | Dot matches newline |
| `VERBOSE` | `x` | Verbose mode |
| `ASCII` | `a` | ASCII-only matching |
| `UNICODE` | `u` | Unicode matching |

---

## 💡 Design Philosophy & Roadmap

### 🏗️ Design Principles
RegexForge-CLI follows these principles:
1. **Zero Dependencies First** - Use Python standard library for maximum compatibility
2. **Terminal Native** - Designed for terminal users, no need to leave command line
3. **Instant Feedback** - Real-time match results for improved productivity

### 📅 Roadmap
- [ ] **v1.1** - Add regex explanation feature
- [ ] **v1.2** - Support regex performance optimization suggestions
- [ ] **v1.3** - Add regex visualization feature
- [ ] **v1.4** - Support batch file testing

---

## 📦 Packaging & Deployment

### Local Development
```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black regexforge/
```

### Build Distribution
```bash
# Build
python -m build

# Upload to PyPI
twine upload dist/*
```

---

## 🤝 Contributing

We welcome all forms of contributions!

### How to Contribute
1. Fork this repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Create Pull Request

### Commit Convention
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test related

---

## 📄 License

This project is licensed under the **MIT License**.

See [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by RegexForge Team
</p>
