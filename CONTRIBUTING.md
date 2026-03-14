# Contributing to NanoBot Health Assistant

首先，感谢你考虑为 NanoBot 健康助理做出贡献！🎉

## 如何贡献

### 报告 Bug

如果你发现了 bug，请通过 [GitHub Issues](https://github.com/yourusername/nanobot-health-assistant/issues) 报告，并包含以下信息：

- 问题的清晰描述
- 复现步骤
- 预期行为 vs 实际行为
- 系统环境（操作系统、Python 版本等）
- 相关日志或错误信息

### 建议新功能

我们欢迎新功能建议！请通过 GitHub Issues 提交，并描述：

- 功能的用途和场景
- 预期的行为
- 可能的实现方案（可选）

### 提交代码

1. **Fork 仓库**
   ```bash
   git clone https://github.com/yourusername/nanobot-health-assistant.git
   cd nanobot-health-assistant
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/bug-description
   ```

3. **安装开发依赖**
   ```bash
   pip install -e ".[dev]"
   ```

4. **编写代码**
   - 遵循 PEP 8 代码规范
   - 添加适当的注释和文档
   - 为新功能编写测试

5. **运行测试**
   ```bash
   python test_health_assistant.py
   # 或
   pytest tests/
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

   提交信息格式：
   - `feat:` 新功能
   - `fix:` 修复 bug
   - `docs:` 文档更新
   - `test:` 测试相关
   - `refactor:` 代码重构
   - `style:` 代码格式

7. **推送到你的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**
   - 描述你做了什么和为什么
   - 关联相关的 Issue（如果有）

## 代码规范

### Python 代码风格

- 使用 [Black](https://github.com/psf/black) 格式化代码
- 最大行长度：100 字符
- 使用类型提示（可选但推荐）

```python
def record_health_metric(
    metric_type: str, 
    value: float, 
    unit: str, 
    note: str = ""
) -> dict:
    """记录健康指标的文档字符串"""
    pass
```

### 文档

- 所有公共函数和类都需要文档字符串
- 使用 Google Style 或 NumPy Style
- 更新 README.md 如果添加了新功能

### 测试

- 为新功能编写测试
- 确保所有测试通过
- 保持测试覆盖率 > 80%

## 开发指南

### 项目结构

```
nanobot-health-assistant/
├── skills/           # 技能定义（SKILL.md 格式）
├── config/           # 配置文件
├── *.py              # 核心模块
├── tests/            # 测试文件
└── docs/             # 文档
```

### 添加新技能

1. 在 `skills/` 下创建新目录
2. 创建 `SKILL.md` 文件
3. 在 `health_data_manager.py` 添加数据操作函数
4. 在 `config/nanobot.config.json` 注册技能
5. 添加测试
6. 更新文档

### 添加可视化功能

1. 在 `visualization.py` 中添加新方法
2. 确保 matplotlib 不可用时有回退方案
3. 添加测试
4. 更新 README

## 行为准则

- 友善和尊重
- 接受建设性批评
- 关注什么对社区最有利
- 显示对他人的同理心

## 问题？

如果你有任何问题，欢迎：

- 查看 [README.md](README.md)
- 查看 [文档](docs/)
- 创建 [GitHub Issue](https://github.com/yourusername/nanobot-health-assistant/issues)

再次感谢你的贡献！🙏
