# GitHub 新账号接管教程（保姆级）

GitHub New Account Onboarding Guide (Step-by-Step)

---

本教程帮助你完成 GitHub 新账号的「身份冷启动」，确保本地 Git 提交正确关联到新账号，并能顺利推送代码。

## 前置准备

1. 已在 GitHub 官网注册新账号（如 `YourNewUsername`）。
2. 已创建仓库（如 `PyDSAI-Arch-Python`），仓库地址：  
   `https://github.com/YourNewUsername/PyDSAI-Arch-Python`
3. 本电脑将主要使用该新账号。

---

## 第一步：配置 Git 本地身份（非常重要！）

提交记录（Commits）需要与 GitHub 账号正确关联，否则绿点不会显示在你的个人主页。

### Windows（PowerShell 或 CMD）

```powershell
# 全局设置：用户名（与 GitHub 用户名一致）
git config --global user.name "你的新GitHub用户名"

# 全局设置：邮箱（必须与 GitHub 账号绑定的邮箱一致）
git config --global user.email "你注册新号用的邮箱"
```

### 示例

```powershell
git config --global user.name "ZhangSan"
git config --global user.email "zhangsan@example.com"
```

### 验证配置

```powershell
git config --global user.name
git config --global user.email
```

应分别输出你设置的用户名和邮箱。

---

## 第二步：生成 SSH Key（避免频繁输密码）

GitHub 推荐使用 SSH 认证，配置一次后即可免密推送。

### 2.1 生成密钥

在终端执行（将邮箱替换为你的邮箱）：

```powershell
ssh-keygen -t ed25519 -C "你的邮箱"
```

提示 `Enter file in which to save the key` 时，直接回车使用默认路径。  
提示 `Enter passphrase` 时，可回车留空，或输入密码增强安全。

### 2.2 查看公钥

```powershell
# Windows PowerShell
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub

# 或 Git Bash / WSL
cat ~/.ssh/id_ed25519.pub
```

复制输出的整行内容（以 `ssh-ed25519` 开头）。

### 2.3 添加到 GitHub

1. 登录 GitHub → 右上角头像 → **Settings**
2. 左侧 **SSH and GPG keys**
3. 点击 **New SSH key**
4. Title 填写例如 `My PC` 或 `Work Laptop`
5. Key 粘贴刚才复制的公钥
6. 点击 **Add SSH key**

### 2.4 测试连接

```powershell
ssh -T git@github.com
```

首次可能提示 `Are you sure you want to continue connecting?`，输入 `yes`。  
成功时会显示：`Hi YourUsername! You've successfully authenticated...`

---

## 第三步：关联并推送项目

### 3.1 进入项目目录

```powershell
cd "c:\Users\吕宇轩\Desktop\PyDSAI"
```

### 3.2 初始化（若尚未初始化）

```powershell
git init
```

若已有 `.git`，此步可跳过。

### 3.3 关联远程仓库

**SSH 地址（推荐）：**

```powershell
git remote add origin git@github.com:你的用户名/PyDSAI-Arch-Python.git
```

**HTTPS 地址（备选）：**

```powershell
git remote add origin https://github.com/你的用户名/PyDSAI-Arch-Python.git
```

将 `你的用户名` 替换为实际 GitHub 用户名。

### 3.4 创建 .gitignore（若不存在）

确保以下内容在 `.gitignore` 中，避免提交无关文件：

```
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
*.egg-info/
venv/
.env
```

### 3.5 提交并推送

```powershell
# 添加所有文件
git add .

# 提交（commit message 可自定义）
git commit -m "chore: Final industrial-grade implementation with BST and Benchmarks"

# 设置主分支为 main
git branch -M main

# 推送到远程（首次需 -u 建立跟踪）
git push -u origin main
```

若远程已有内容且历史不同，可能需要：

```powershell
git pull origin main --rebase
git push -u origin main
```

---

## 常见问题

### Q1: `Permission denied (publickey)` 或 `Could not read from remote repository`

- 确认已添加 SSH 公钥到 GitHub  
- 再次执行 `ssh -T git@github.com` 测试

### Q2: `Support for password authentication was removed`

- 必须使用 SSH 或 Personal Access Token，不能再用账号密码  
- 推荐使用 SSH，按本教程第二步配置

### Q3: 想用 HTTPS 且免密

- 使用 [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager)  
- 或配置 Personal Access Token 作为密码

### Q4: 已有 origin，想更换远程地址

```powershell
git remote remove origin
git remote add origin git@github.com:你的用户名/PyDSAI-Arch-Python.git
```

---

## 检查清单

- [ ] `git config user.name` 与 GitHub 用户名一致
- [ ] `git config user.email` 与 GitHub 绑定邮箱一致
- [ ] SSH 公钥已添加到 GitHub
- [ ] `ssh -T git@github.com` 认证成功
- [ ] `git remote -v` 显示正确的 origin 地址
- [ ] `git push -u origin main` 推送成功

完成以上步骤后，你的新账号即可正常使用，提交会正确显示在个人主页的绿点中。
