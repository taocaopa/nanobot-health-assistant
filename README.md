# 🏥 NanoBot 个人健康助理

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/yourusername/nanobot-health-assistant/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/yourusername/nanobot-health-assistant/actions)

基于 [NanoBot](https://github.com/HKUDS/nanobot) 框架的 WhatsApp AI 健康助理机器人，帮助您全面管理日常健康。

![Health Assistant Demo](docs/demo.png)

## ✨ 功能特性

### 📊 健康数据管理
- **体重追踪** - 记录体重变化，生成趋势图表
- **血压监测** - 记录血压数据，识别异常
- **心率记录** - 追踪静息心率和运动心率
- **血糖管理** - 记录空腹和餐后血糖
- **综合指标** - BMI、体脂率等健康指标

### 🍎 饮食追踪
- **三餐记录** - 记录每日饮食内容
- **卡路里估算** - 智能估算食物热量
- **营养分析** - 分析营养摄入平衡
- **饮水记录** - 追踪每日饮水量
- **饮食建议** - 基于数据提供改善建议

### 🏃 运动记录
- **运动日志** - 记录各类运动活动
- **卡路里计算** - 计算运动消耗
- **运动目标** - 设定和追踪运动目标
- **强度分析** - 分析运动强度和效果
- **周报生成** - 自动生成运动周报告

### 🤒 症状追踪
- **症状记录** - 记录身体不适症状
- **严重程度** - 评估和追踪症状严重程度
- **触发因素** - 识别症状触发因素
- **模式分析** - 发现症状规律
- **就医建议** - 异常时建议就医

### 😴 睡眠分析
- **睡眠记录** - 记录睡眠时长和质量
- **效率分析** - 计算睡眠效率
- **睡眠评分** - 1-10分睡眠质量评分
- **影响因素** - 分析影响睡眠的因素
- **改善建议** - 提供睡眠改善方案

### 👟 步数追踪
- **步数记录** - 记录每日步数
- **距离计算** - 估算行走距离
- **目标设定** - 设定每日步数目标
- **成就系统** - 解锁健康成就
- **趋势分析** - 分析活动趋势

### ⏰ 健康提醒
- **用药提醒** - 定时提醒服药
- **喝水提醒** - 定时提醒饮水
- **运动提醒** - 提醒运动时间
- **休息提醒** - 提醒休息眼睛
- **睡眠提醒** - 提醒就寝时间

### 📈 数据可视化
- **趋势图表** - 生成健康趋势图
- **周报/月报** - 自动生成健康报告
- **HTML 报告** - 美观的网页版报告
- **数据导出** - 支持导出数据
- **隐私保护** - 所有数据本地存储

## 🚀 快速开始

### 前置要求

- Python 3.8+
- NanoBot 框架
- OpenRouter API Key（或其他 LLM Provider）

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/nanobot-health-assistant.git
cd nanobot-health-assistant

# 安装依赖
pip install -r requirements.txt

# 或一键部署
chmod +x deploy.sh
./deploy.sh
```

### 2. 配置 API Key

```bash
# 初始化 NanoBot 配置
nanobot onboard
```

编辑配置文件 `~/.nanobot/config.json`:

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-你的API密钥"
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-3.5-sonnet",
      "provider": "openrouter"
    }
  }
}
```

获取 API Key: [OpenRouter](https://openrouter.ai/keys)

### 3. 复制健康助理配置

```bash
# 复制配置
cp config/nanobot.config.json ~/.nanobot/config.json
```

### 4. 连接 WhatsApp

```bash
# 连接 WhatsApp
nanobot channels login

# 扫描终端显示的二维码
```

### 5. 启动服务

```bash
# 启动 Gateway
nanobot gateway

# 现在可以在 WhatsApp 中与你的健康助理对话了！
```

## 💬 使用示例

### 健康数据记录

```
你: 记录体重 70.5kg
助理: ✅ 已记录！你今天的体重是 70.5kg，比上次减少了 0.3kg，继续加油！💪

你: 记录血压 120/80
助理: ✅ 血压已记录：收缩压 120 mmHg，舒张压 80 mmHg，在正常范围内。

你: 记录睡眠 7.5小时，质量很好，11点睡6点半起
助理: 🌙 睡眠已记录！时长 7.5 小时，质量评分 8/10，睡眠效率很高！
```

### 饮食追踪

```
你: 早餐吃了燕麦、鸡蛋和牛奶
助理: 🍳 早餐已记录！估算约 450 卡路里

你: 今天走了多少步？
助理: 👟 今天已走 8,500 步，完成目标的 85%，还差 1,500 步达标！

你: 生成本周健康报告
助理: 📊 正在生成本周健康报告...
      [发送详细的文字报告和图表]
```

### 症状追踪

```
你: 头痛，程度中等，在前额位置，可能是看电脑太久
助理: ✅ 症状已记录。建议你：
      1. 休息一下，离开屏幕 10 分钟
      2. 做眼保健操
      3. 多喝水
      4. 如果持续不缓解，建议就医检查

你: 分析我的头痛模式
助理: 📊 根据最近 30 天的记录：
      - 头痛多发生在下午 2-4 点
      - 常见触发因素：长时间看屏幕（80%）、睡眠不足（60%）
      - 建议：每小时休息眼睛，保证 7-8 小时睡眠
```

### 数据可视化

```
你: 生成体重趋势图
助理: 📈 [发送体重变化趋势图]
      过去 30 天体重变化：
      - 起始：72.0 kg
      - 当前：70.5 kg
      - 变化：-1.5 kg ⬇️
      - 趋势：稳步下降，继续保持！

你: 显示睡眠分析
助理: 😴 [发送睡眠质量图表]
      本周睡眠统计：
      - 平均时长：7.2 小时
      - 平均质量：7.5/10
      - 最佳入睡时间：22:30
      - 建议：保持规律作息
```

## 📁 项目结构

```
nanobot-health-assistant/
├── 📁 skills/                          # 健康技能模块
│   ├── health_data/SKILL.md           # 健康数据管理
│   ├── diet_tracker/SKILL.md          # 饮食追踪
│   ├── exercise_log/SKILL.md          # 运动记录
│   ├── symptom_tracker/SKILL.md       # 症状追踪
│   ├── sleep_analyzer/SKILL.md        # 睡眠分析 ⭐ NEW
│   ├── step_tracker/SKILL.md          # 步数追踪 ⭐ NEW
│   └── health_reminder/SKILL.md       # 健康提醒
├── 📁 config/                          # 配置文件
│   ├── nanobot.config.json            # NanoBot 配置
│   └── health_persona.md              # 助理人设
├── 📁 .github/workflows/               # CI/CD 配置
│   └── ci.yml                         # GitHub Actions
├── health_data_manager.py             # 数据管理模块
├── visualization.py                   # 可视化模块 ⭐ NEW
├── test_health_assistant.py           # 测试脚本
├── deploy.sh                          # 部署脚本
├── setup.py                           # 包配置
├── requirements.txt                   # 依赖列表
├── .gitignore                         # Git 忽略规则
└── README.md                          # 本文件
```

## 🔧 高级配置

### 自定义提醒

编辑 `~/.nanobot/config.json` 中的 `cron` 部分：

```json
{
  "cron": {
    "enabled": true,
    "jobs": [
      {
        "name": "water_reminder",
        "schedule": "0 */2 * * *",
        "message": "💧 喝水时间！起来活动一下~"
      },
      {
        "name": "bedtime_reminder",
        "schedule": "0 22 * * *",
        "message": "🌙 该准备睡觉了，保证充足睡眠哦~"
      }
    ]
  }
}
```

### 修改步数目标

```bash
# 设置每日步数目标
# 在 WhatsApp 中发送：
"设置每天 12000 步的目标"
```

### 睡眠目标

```bash
# 设置睡眠目标
# 在 WhatsApp 中发送：
"设定每天睡 8 小时，10 点半睡觉"
```

## 📊 数据可视化

### 生成图表

```python
from visualization import HealthVisualizer

viz = HealthVisualizer()

# 生成体重趋势图
viz.generate_weight_chart(days=30)

# 生成睡眠分析图
viz.generate_sleep_chart(days=14)

# 生成步数图表
viz.generate_steps_chart(days=14)

# 生成完整周报
viz.generate_weekly_report()

# 生成 HTML 报告
viz.generate_html_report(days=7)
```

### 图表输出位置

所有生成的图表和报告保存在 `reports/` 目录：
- `weight_chart_YYYYMMDD.png` - 体重趋势图
- `sleep_chart_YYYYMMDD.png` - 睡眠质量图
- `steps_chart_YYYYMMDD.png` - 步数统计图
- `weekly_report_YYYYMMDD.txt` - 文字周报
- `health_report_YYYYMMDD.html` - 网页版报告

## 🧪 测试

```bash
# 运行所有测试
python test_health_assistant.py

# 或使用 pytest
pytest tests/ -v
```

## 🔒 隐私与安全

- ✅ **本地存储** - 所有健康数据存储在 `~/.nanobot/data/`，不上传云端
- ✅ **数据加密** - 支持可选的数据加密（需额外配置）
- ✅ **隐私保护** - 你的健康数据只属于你
- ✅ **定期备份** - 建议定期备份 `~/.nanobot/data/` 目录

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 开发环境设置

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 代码格式化
black .

# 代码检查
flake8 .
```

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解详细更新历史。

## ⚠️ 免责声明

本健康助理**仅供参考**，**不能替代专业医疗建议**。提供的所有健康建议基于一般医学知识，不针对个人具体情况。如有健康问题，请务必咨询专业医生。

**以下情况请立即就医：**
- 胸痛或胸闷
- 呼吸困难
- 严重腹痛
- 持续高烧
- 意识模糊

## 📄 License

本项目采用 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

- [HKUDS/nanobot](https://github.com/HKUDS/nanobot) - NanoBot 框架
- [OpenClaw](https://github.com/openclaw/openclaw) - 原始 OpenClaw 项目
- [OpenRouter](https://openrouter.ai/) - LLM API 服务

## 📞 支持

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/yourusername/nanobot-health-assistant/issues)
- 发送邮件到: health@example.com

---

⭐ 如果这个项目对你有帮助，请给它一个 Star！
