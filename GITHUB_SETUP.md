# GitHub 仓库设置指南

## 快速设置

### 1. 在 GitHub 上创建仓库

访问: https://github.com/new

设置:
- **Repository name**: `nanobot-health-assistant`
- **Description**: 基于 NanoBot 的个人健康管理 WhatsApp 机器人
- **Visibility**: Public（或 Private）
- **Initialize**: 不要勾选（已初始化）

### 2. 推送本地代码

在终端执行以下命令：

```bash
cd /workspace/projects/nanobot-health

# 添加远程仓库（替换 yourusername 为你的 GitHub 用户名）
git remote add origin https://github.com/yourusername/nanobot-health-assistant.git

# 推送到 GitHub
git push -u origin main

# 推送标签
git push origin v1.0.0
```

### 3. 验证

访问: `https://github.com/yourusername/nanobot-health-assistant`

你应该能看到所有文件和提交历史。

---

## 高级设置

### 设置 GitHub Secrets（用于 CI/CD）

如果需要自动发布到 PyPI：

1. 访问: `https://github.com/yourusername/nanobot-health-assistant/settings/secrets/actions`
2. 点击 "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: 你的 PyPI API Token
5. 点击 "Add secret"

获取 PyPI Token: https://pypi.org/manage/account/token/

### 启用 GitHub Pages（可选）

用于托管文档：

1. 访问: `https://github.com/yourusername/nanobot-health-assistant/settings/pages`
2. Source: Deploy from a branch
3. Branch: main / docs (或创建 docs 分支)
4. 点击 Save

### 添加 Topics

在仓库页面右侧点击齿轮图标，添加 topics:
- health
- fitness
- nanobot
- whatsapp
- ai-assistant
- python
- health-tracking

---

## 本地 Git 配置

如果你还没有配置 Git：

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 常用 Git 命令

```bash
# 查看状态
git status

# 查看提交历史
git log --oneline

# 创建新分支
git checkout -b feature/new-feature

# 合并分支
git checkout main
git merge feature/new-feature

# 推送分支
git push origin feature/new-feature

# 拉取更新
git pull origin main

# 查看远程仓库
git remote -v
```

---

## 问题解决

### 推送被拒绝

```bash
# 如果远程仓库已存在文件，先拉取
git pull origin main --rebase
# 然后推送
git push origin main
```

### 认证问题

```bash
# 使用 HTTPS 并缓存凭证
git config --global credential.helper cache

# 或使用 SSH（推荐）
git remote set-url origin git@github.com:yourusername/nanobot-health-assistant.git
```

---

## 下一步

1. ✅ 推送代码到 GitHub
2. ✅ 启用 GitHub Actions
3. ⏭️ 邀请协作者（可选）
4. ⏭️ 设置分支保护规则
5. ⏭️ 创建 Project Board 管理任务

---

祝你使用愉快！🎉
