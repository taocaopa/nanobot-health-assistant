# NanoBot 健康助理 - 系统架构设计

## 1. 架构概述

### 1.1 项目定位
**NanoBot Health Assistant** 是一个基于 NanoBot 框架的轻量化 AI 健康管理系统，通过 WhatsApp 提供自然语言交互界面，实现个人健康数据的记录、分析和可视化。

### 1.2 架构原则

```
┌─────────────────────────────────────────────────────────────┐
│                    架构设计原则                              │
├─────────────────────────────────────────────────────────────┤
│ 1. 模块化 (Modularity)     - 单一职责，独立部署              │
│ 2. 可扩展 (Scalability)    - 插件化技能系统                  │
│ 3. 隐私优先 (Privacy First) - 本地数据存储                   │
│ 4. 低耦合 (Loose Coupling) - 事件驱动架构                    │
│ 5. 高内聚 (High Cohesion)  - 功能内聚设计                    │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 技术栈选型

| 层级 | 技术 | 选型理由 |
|------|------|---------|
| **框架** | NanoBot | 轻量级，比 OpenClaw 减少 99% 代码 |
| **通信** | WhatsApp | 用户熟悉，无需额外安装 App |
| **AI** | OpenRouter | 统一 API，支持多模型 |
| **存储** | JSON 文件 | 简单，无需数据库，保护隐私 |
| **可视化** | Matplotlib | Python 标准，易于集成 |
| **CI/CD** | GitHub Actions | 自动化测试和发布 |

---

## 2. 系统架构图

```
┌────────────────────────────────────────────────────────────────┐
│                         用户层 (User Layer)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   WhatsApp   │  │   Telegram   │  │   Web UI     │         │
│  │   (主要)     │  │   (未来)     │  │   (未来)     │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
└─────────┼──────────────────┼──────────────────┼────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
┌────────────────────────────┼──────────────────────────────────┐
│                    接入层 (Gateway Layer)                     │
│  ┌─────────────────────────┴──────────────────────────────┐  │
│  │              NanoBot Gateway (Port 5000)               │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │  │
│  │  │   WebSocket │  │   Webhook   │  │   REST API  │   │  │
│  │  │   Handler   │  │   Handler   │  │   Handler   │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┼──────────────────────────────────┐
│                   核心层 (Core Layer)                         │
│  ┌─────────────────────────┴──────────────────────────────┐  │
│  │                   AI Agent Core                         │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │  │
│  │  │   Intent    │  │   Context   │  │  Response   │   │  │
│  │  │  Recognition│  │   Manager   │  │  Generator  │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┼──────────────────────────────────┐
│                  技能层 (Skills Layer)                        │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐   │
│  │ health_data │diet_tracker │exercise_log │sleep_analyzer│  │
│  │    (健康)   │   (饮食)    │   (运动)    │   (睡眠)    │  │
│  └─────────────┴─────────────┴─────────────┴─────────────┘   │
│  ┌─────────────┬─────────────┬─────────────┐                 │
│  │step_tracker │symptom_     │health_      │                 │
│  │   (步数)    │  tracker    │ reminder    │                 │
│  │             │  (症状)     │  (提醒)     │                 │
│  └─────────────┴─────────────┴─────────────┘                 │
└───────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┼──────────────────────────────────┐
│                  数据层 (Data Layer)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │   Health    │  │    Diet     │  │      Exercise       │   │
│  │   Metrics   │  │    Logs     │  │       Logs          │   │
│  │  (JSON)     │  │   (JSON)    │  │      (JSON)         │   │
│  └─────────────┘  └─────────────┘  └─────────────────────┘   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │    Sleep    │  │    Step     │  │    Symptom          │   │
│  │    Logs     │  │    Logs     │  │      Logs           │   │
│  │  (JSON)     │  │   (JSON)    │  │     (JSON)          │   │
│  └─────────────┘  └─────────────┘  └─────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Visualization & Reports                    │ │
│  │         (Charts, HTML Reports, Analytics)               │ │
│  └─────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

---

## 3. 核心组件详解

### 3.1 Agent Core (智能体核心)

```python
# 架构示意图
class HealthAssistantAgent:
    """
    健康助理智能体核心
    职责: 意图识别、上下文管理、响应生成
    """
    
    def __init__(self):
        self.intent_recognizer = IntentRecognizer()
        self.context_manager = ContextManager()
        self.skill_router = SkillRouter()
        self.response_generator = ResponseGenerator()
    
    def process(self, user_input: str) -> str:
        # 1. 意图识别
        intent = self.intent_recognizer.recognize(user_input)
        
        # 2. 加载上下文
        context = self.context_manager.load(intent.session_id)
        
        # 3. 路由到技能
        skill_response = self.skill_router.route(intent, context)
        
        # 4. 生成响应
        response = self.response_generator.generate(skill_response)
        
        # 5. 更新上下文
        self.context_manager.update(intent.session_id, context)
        
        return response
```

### 3.2 技能系统 (Skills System)

每个技能遵循 **SKILL.md** 规范，包含：

```yaml
# 技能元数据
name: sleep-analyzer
description: 睡眠分析和追踪工具
version: 1.0.0
author: AI Architect

# 技能能力
capabilities:
  - record_sleep
  - analyze_sleep_patterns
  - generate_sleep_report
  
# 依赖关系
dependencies:
  - health_data_manager
  - visualization
```

### 3.3 数据管理模块

```python
# 数据流示意图
class HealthDataManager:
    """
    统一数据管理接口
    采用 Repository 模式
    """
    
    # 数据存储路径
    DATA_DIR = "~/.nanobot/data"
    
    def __init__(self):
        self.repositories = {
            'health': HealthRepository(),
            'diet': DietRepository(),
            'exercise': ExerciseRepository(),
            'sleep': SleepRepository(),
            'step': StepRepository(),
            'symptom': SymptomRepository(),
        }
    
    def save(self, domain: str, data: dict) -> bool:
        """统一保存接口"""
        return self.repositories[domain].save(data)
    
    def query(self, domain: str, filters: dict) -> list:
        """统一查询接口"""
        return self.repositories[domain].query(filters)
```

---

## 4. 数据流设计

### 4.1 请求处理流程

```
用户输入
    │
    ▼
┌──────────────────┐
│  1. 预处理        │  ← 清洗、分词、实体识别
│  Pre-processing  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  2. 意图识别      │  ← NLP 模型分析意图
│  Intent Recog.   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  3. 实体抽取      │  ← 提取关键信息
│  Entity Extract  │     (数值、时间、类型)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  4. 技能匹配      │  ← 路由到对应技能
│  Skill Routing   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  5. 业务处理      │  ← 执行具体业务逻辑
│  Business Logic  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  6. 响应生成      │  ← 格式化输出
│  Response Gen.   │
└────────┬─────────┘
         │
         ▼
    返回给用户
```

### 4.2 数据持久化流程

```
业务逻辑
    │
    ▼
┌──────────────────┐
│  Data Validation │  ← 验证数据格式
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Data Transform  │  ← 转换为存储格式
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  File I/O        │  ← 写入 JSON 文件
│  (Atomic Write)  │     原子操作防损坏
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Cache Update    │  ← 更新内存缓存
└──────────────────┘
```

---

## 5. 扩展性设计

### 5.1 新技能添加流程

```
Step 1: 定义 SKILL.md
    ↓
Step 2: 实现数据操作函数
    ↓
Step 3: 注册到 config/nanobot.config.json
    ↓
Step 4: 编写测试用例
    ↓
Step 5: 更新文档
    ↓
Step 6: 部署上线
```

### 5.2 多渠道支持架构

```python
# 渠道抽象层
class ChannelAdapter:
    """渠道适配器基类"""
    
    def send_message(self, user_id: str, message: str):
        raise NotImplementedError
    
    def receive_message(self) -> Message:
        raise NotImplementedError

class WhatsAppAdapter(ChannelAdapter):
    """WhatsApp 渠道实现"""
    pass

class TelegramAdapter(ChannelAdapter):
    """Telegram 渠道实现（未来）"""
    pass

class WebAdapter(ChannelAdapter):
    """Web 渠道实现（未来）"""
    pass
```

---

## 6. 安全设计

### 6.1 数据安全

```
┌─────────────────────────────────────────┐
│            数据安全策略                  │
├─────────────────────────────────────────┤
│ 1. 本地存储                              │
│    - 所有数据存储在用户本地 ~/.nanobot/  │
│    - 不上传云端，保护隐私                │
│                                         │
│ 2. 访问控制                              │
│    - 文件权限 600 (仅所有者可读写)       │
│    - 数据隔离，多用户不冲突              │
│                                         │
│ 3. 备份策略                              │
│    - 定期自动备份                        │
│    - 导出功能支持                        │
└─────────────────────────────────────────┘
```

### 6.2 API 安全

- Token 存储在环境变量，不提交到代码
- 使用 HTTPS 通信
- 定期轮换 API Key

---

## 7. 性能优化

### 7.1 缓存策略

```python
# 多层缓存
class CacheManager:
    def __init__(self):
        self.l1_cache = {}  # 内存缓存 (LRU)
        self.l2_cache = None  # 未来: Redis
    
    def get(self, key: str):
        # L1 缓存
        if key in self.l1_cache:
            return self.l1_cache[key]
        
        # 加载到缓存
        value = self.load_from_disk(key)
        self.l1_cache[key] = value
        return value
```

### 7.2 懒加载

```python
# 按需加载数据
class LazyDataLoader:
    def __init__(self):
        self._data = None
    
    @property
    def data(self):
        if self._data is None:
            self._data = self._load_data()
        return self._data
```

---

## 8. 监控与日志

### 8.1 日志架构

```
Application Logs
    │
    ├── Error Logs    → 错误追踪
    ├── Access Logs   → 访问统计  
    ├── Debug Logs    → 调试信息
    └── Audit Logs    → 审计记录
```

### 8.2 健康检查

```python
# 健康检查端点
class HealthChecker:
    def check(self) -> HealthStatus:
        return {
            'database': self.check_database(),
            'api': self.check_api_connectivity(),
            'disk': self.check_disk_space(),
            'memory': self.check_memory_usage(),
        }
```

---

## 9. 部署架构

### 9.1 单机部署

```
┌─────────────────────────────────────────┐
│              单机部署模式                │
├─────────────────────────────────────────┤
│                                         │
│   ┌─────────────────────────────────┐  │
│   │         服务器/PC                │  │
│   │  ┌───────────────────────────┐ │  │
│   │  │    NanoBot Gateway        │ │  │
│   │  │    (Port 5000)            │ │  │
│   │  └───────────────────────────┘ │  │
│   │              │                  │  │
│   │  ┌───────────────────────────┐ │  │
│   │  │    Health Assistant       │ │  │
│   │  │    (Business Logic)       │ │  │
│   │  └───────────────────────────┘ │  │
│   │              │                  │  │
│   │  ┌───────────────────────────┐ │  │
│   │  │    Local Data Storage     │ │  │
│   │  │    (~/.nanobot/data/)     │ │  │
│   │  └───────────────────────────┘ │  │
│   └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

### 9.2 Docker 部署 (未来)

```dockerfile
# Dockerfile 示例
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["nanobot", "gateway"]
```

---

## 10. 总结

本架构设计遵循以下核心思想：

1. **简单至上** - 使用 JSON 文件存储，避免复杂数据库
2. **隐私优先** - 本地存储，不上传云端
3. **模块化** - 技能可插拔，易于扩展
4. **可测试** - 每个模块独立测试
5. **文档驱动** - SKILL.md 即文档即代码

这种架构适合个人开发者快速构建 AI 应用，同时保持足够的扩展性应对未来需求。

---

*文档版本: 1.0.0*  
*作者: Chief AI Architect*  
*日期: 2026-03-15*
