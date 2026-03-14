# AI 工程师培训 - 构建 NanoBot 健康助理

## 培训目标

本培训文档面向 AI 工程师和机器工程师，通过实战项目掌握：
- AI Agent 架构设计
- 自然语言处理 (NLP) 在健康领域的应用
- 模块化系统设计
- 测试驱动开发 (TDD)
- 生产环境部署

---

## 第一阶段：理论基础 (Day 1-2)

### 1.1 AI Agent 架构原理

#### 什么是 AI Agent?

```
传统软件:
输入 → [固定规则] → 输出

AI Agent:
输入 → [感知 → 理解 → 决策 → 执行] → 输出
              ↑___________↓
                  反馈循环
```

#### Agent 核心组件

```python
class AIAgent:
    """
    AI Agent 标准架构
    """
    def __init__(self):
        self.perception = PerceptionModule()    # 感知层
        self.understanding = NLPUnderstanding() # 理解层
        self.reasoning = ReasoningEngine()      # 推理层
        self.action = ActionExecutor()          # 执行层
        self.memory = MemoryStore()             # 记忆层
    
    def run(self, input_data):
        # 1. 感知
        perceived = self.perception.process(input_data)
        
        # 2. 理解
        understood = self.understanding.parse(perceived)
        
        # 3. 检索记忆
        context = self.memory.retrieve(understood)
        
        # 4. 推理决策
        decision = self.reasoning.decide(understood, context)
        
        # 5. 执行动作
        result = self.action.execute(decision)
        
        # 6. 更新记忆
        self.memory.store(input_data, result)
        
        return result
```

### 1.2 意图识别 (Intent Recognition)

#### 基于规则的意图识别

```python
class RuleBasedIntentRecognizer:
    """
    基于规则的意图识别器
    适合领域明确、意图清晰的场景
    """
    
    RULES = {
        'record_weight': {
            'patterns': [
                r'记录.*体重',
                r'体重.*(\d+\.?\d*)',
                r'称重',
            ],
            'entities': ['weight']
        },
        'record_sleep': {
            'patterns': [
                r'记录.*睡眠',
                r'睡了.*(\d+)小时',
                r'昨晚.*睡眠',
            ],
            'entities': ['duration', 'quality']
        },
        'query_stats': {
            'patterns': [
                r'查看.*统计',
                r'最近.*数据',
                r'趋势.*如何',
            ],
            'entities': ['time_range', 'metric']
        }
    }
    
    def recognize(self, text: str) -> Intent:
        """识别意图"""
        for intent_name, config in self.RULES.items():
            for pattern in config['patterns']:
                if re.search(pattern, text):
                    return Intent(
                        name=intent_name,
                        confidence=1.0,
                        entities=self.extract_entities(text, config['entities'])
                    )
        
        return Intent(name='unknown', confidence=0.0)
```

#### 基于机器学习的意图识别

```python
class MLIntentRecognizer:
    """
    基于机器学习的意图识别
    适合复杂、模糊的场景
    """
    
    def __init__(self):
        # 使用预训练模型
        from transformers import pipeline
        self.classifier = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
    
    def recognize(self, text: str) -> Intent:
        """使用模型预测意图"""
        result = self.classifier(text)[0]
        return Intent(
            name=result['label'],
            confidence=result['score']
        )
```

### 1.3 实体抽取 (Named Entity Recognition)

```python
class HealthEntityExtractor:
    """
    健康领域实体抽取器
    """
    
    # 实体模式定义
    PATTERNS = {
        'WEIGHT': {
            'pattern': r'(\d+\.?\d*)\s*(kg|公斤|千克|斤)',
            'converter': lambda m: float(m.group(1)) if m.group(2) != '斤' else float(m.group(1)) / 2
        },
        'DURATION': {
            'pattern': r'(\d+\.?\d*)\s*(小时|h|分钟|min)',
            'converter': lambda m: float(m.group(1)) if m.group(2) in ['小时', 'h'] else float(m.group(1)) / 60
        },
        'TIME': {
            'pattern': r'(\d{1,2}):(\d{2})',
            'converter': lambda m: f"{m.group(1).zfill(2)}:{m.group(2)}"
        },
        'DATE': {
            'pattern': r'(\d{4})-(\d{2})-(\d{2})',
            'converter': lambda m: f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        }
    }
    
    def extract(self, text: str) -> List[Entity]:
        """抽取所有实体"""
        entities = []
        
        for entity_type, config in self.PATTERNS.items():
            for match in re.finditer(config['pattern'], text):
                entity = Entity(
                    type=entity_type,
                    raw_value=match.group(0),
                    normalized_value=config['converter'](match),
                    start=match.start(),
                    end=match.end()
                )
                entities.append(entity)
        
        return entities


# 使用示例
extractor = HealthEntityExtractor()
text = "我体重 70.5kg，昨晚睡了 7.5 小时"
entities = extractor.extract(text)

for entity in entities:
    print(f"{entity.type}: {entity.normalized_value}")
# 输出:
# WEIGHT: 70.5
# DURATION: 7.5
```

---

## 第二阶段：实战开发 (Day 3-5)

### 2.1 开发任务分解

```
项目: NanoBot 健康助理
├── Task 1: 项目初始化 (1h)
│   ├── 创建项目结构
│   ├── 配置开发环境
│   └── 初始化 Git
│
├── Task 2: 数据管理模块 (3h)
│   ├── 设计数据模型
│   ├── 实现 Repository 模式
│   └── 编写单元测试
│
├── Task 3: 第一个技能 - 体重追踪 (2h)
│   ├── 编写 SKILL.md
│   ├── 实现业务逻辑
│   └── 集成测试
│
├── Task 4: 意图识别模块 (3h)
│   ├── 设计意图分类
│   ├── 实现规则引擎
│   └── 实体抽取
│
├── Task 5: 响应生成模块 (2h)
│   ├── 设计模板系统
│   ├── 实现渲染引擎
│   └── 多语言支持
│
├── Task 6: 可视化模块 (4h)
│   ├── 图表生成
│   ├── 报告系统
│   └── HTML 导出
│
├── Task 7: 集成测试 (2h)
│   ├── 端到端测试
│   ├── 性能测试
│   └── 修复 Bug
│
└── Task 8: 部署上线 (1h)
    ├── 编写部署脚本
    ├── 配置监控
    └── 发布文档
```

### 2.2 Task 2: 数据管理模块实战

#### Step 1: 设计数据模型

```python
# models.py
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List
import json

@dataclass
class HealthRecord:
    """健康记录基类"""
    id: str
    created_at: datetime
    updated_at: datetime
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)


@dataclass
class WeightRecord(HealthRecord):
    """体重记录"""
    value: float          # 体重值
    unit: str            # 单位 (kg, lb)
    measured_at: datetime # 测量时间
    note: Optional[str] = None
    
    @property
    def bmi(self, height_m: float) -> float:
        """计算 BMI"""
        return self.value / (height_m ** 2)


@dataclass
class SleepRecord(HealthRecord):
    """睡眠记录"""
    duration: float       # 睡眠时长 (小时)
    quality_score: int    # 质量评分 1-10
    bedtime: str         # 就寝时间 HH:MM
    wakeup_time: str     # 起床时间 HH:MM
    deep_sleep_percent: Optional[float] = None
    notes: Optional[str] = None
    
    @property
    def efficiency(self) -> float:
        """计算睡眠效率"""
        # 在床时间 = 起床时间 - 就寝时间
        # 睡眠效率 = 睡眠时长 / 在床时间
        bed_hour = int(self.bedtime.split(':')[0])
        wake_hour = int(self.wakeup_time.split(':')[0])
        
        if wake_hour < bed_hour:  # 跨夜
            wake_hour += 24
        
        time_in_bed = wake_hour - bed_hour
        return (self.duration / time_in_bed) * 100 if time_in_bed > 0 else 0
```

#### Step 2: 实现 Repository

```python
# repositories.py
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from pathlib import Path
import json

T = TypeVar('T', bound=HealthRecord)


class Repository(ABC, Generic[T]):
    """Repository 抽象基类"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """确保文件存在"""
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def _load_all(self) -> List[dict]:
        """加载所有数据"""
        with open(self.file_path, 'r') as f:
            return json.load(f)
    
    def _save_all(self, data: List[dict]):
        """保存所有数据"""
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    @abstractmethod
    def to_model(self, data: dict) -> T:
        """字典转模型"""
        pass
    
    @abstractmethod
    def to_dict(self, model: T) -> dict:
        """模型转字典"""
        pass
    
    def create(self, model: T) -> T:
        """创建记录"""
        data = self._load_all()
        data.append(self.to_dict(model))
        self._save_all(data)
        return model
    
    def get_all(self) -> List[T]:
        """获取所有记录"""
        data = self._load_all()
        return [self.to_model(d) for d in data]
    
    def get_by_id(self, record_id: str) -> Optional[T]:
        """根据 ID 获取"""
        data = self._load_all()
        for item in data:
            if item.get('id') == record_id:
                return self.to_model(item)
        return None


class WeightRepository(Repository[WeightRecord]):
    """体重数据仓库"""
    
    def to_model(self, data: dict) -> WeightRecord:
        return WeightRecord(
            id=data['id'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            value=data['value'],
            unit=data['unit'],
            measured_at=datetime.fromisoformat(data['measured_at']),
            note=data.get('note')
        )
    
    def to_dict(self, model: WeightRecord) -> dict:
        return {
            'id': model.id,
            'created_at': model.created_at.isoformat(),
            'updated_at': model.updated_at.isoformat(),
            'value': model.value,
            'unit': model.unit,
            'measured_at': model.measured_at.isoformat(),
            'note': model.note
        }
    
    def get_recent(self, days: int = 7) -> List[WeightRecord]:
        """获取最近记录"""
        all_records = self.get_all()
        cutoff = datetime.now() - timedelta(days=days)
        return [
            r for r in all_records
            if r.measured_at > cutoff
        ]
```

#### Step 3: 编写单元测试

```python
# test_repositories.py
import unittest
import tempfile
from pathlib import Path
from datetime import datetime


class TestWeightRepository(unittest.TestCase):
    """体重仓库测试"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "weight.json"
        self.repo = WeightRepository(self.file_path)
    
    def tearDown(self):
        """测试后清理"""
        self.temp_dir.cleanup()
    
    def test_create(self):
        """测试创建记录"""
        record = WeightRecord(
            id="test-1",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            value=70.5,
            unit='kg',
            measured_at=datetime.now()
        )
        
        result = self.repo.create(record)
        
        self.assertEqual(result.value, 70.5)
        self.assertTrue(self.file_path.exists())
    
    def test_get_recent(self):
        """测试获取最近记录"""
        # 创建测试数据
        now = datetime.now()
        for i in range(10):
            record = WeightRecord(
                id=f"test-{i}",
                created_at=now,
                updated_at=now,
                value=70.0 + i,
                unit='kg',
                measured_at=now - timedelta(days=i)
            )
            self.repo.create(record)
        
        # 获取最近 5 天
        recent = self.repo.get_recent(days=5)
        
        self.assertEqual(len(recent), 5)
        self.assertEqual(recent[0].value, 70.0)  # 最新的
        self.assertEqual(recent[-1].value, 74.0)  # 最早的
    
    def test_bmi_calculation(self):
        """测试 BMI 计算"""
        record = WeightRecord(
            id="test-1",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            value=70.0,
            unit='kg',
            measured_at=datetime.now()
        )
        
        bmi = record.bmi(height_m=1.75)
        
        self.assertAlmostEqual(bmi, 22.86, places=2)


if __name__ == '__main__':
    unittest.main()
```

### 2.3 Task 4: 意图识别实战

#### 练习: 实现睡眠记录意图识别

```python
# intent_recognition_exercise.py
"""
练习: 实现睡眠记录意图识别

目标: 让系统能识别以下输入:
- "昨晚睡了8小时"
- "记录睡眠: 11点睡，6点起"
- "睡眠质量不错，睡了7.5小时"
- "失眠了，只睡了3小时"
"""

class SleepIntentRecognizer:
    """睡眠意图识别器"""
    
    def __init__(self):
        # TODO: 定义匹配模式
        self.patterns = [
            # 模式 1: "睡了X小时"
            r'睡了\s*(\d+\.?\d*)\s*小时',
            # 模式 2: "睡眠 X 小时"
            r'睡眠.*?(\d+\.?\d*)\s*小时',
            # 模式 3: "睡了X个小时"
            r'睡了\s*(\d+\.?\d*)\s*个?小时',
        ]
    
    def recognize(self, text: str) -> dict:
        """
        识别意图
        
        返回:
            {
                'intent': 'record_sleep',
                'confidence': 0.95,
                'entities': {
                    'duration': 8.0,
                    'quality': None
                }
            }
        """
        # TODO: 实现识别逻辑
        pass
    
    def extract_duration(self, text: str) -> Optional[float]:
        """抽取睡眠时长"""
        # TODO: 实现时长抽取
        pass
    
    def extract_quality(self, text: str) -> Optional[int]:
        """抽取睡眠质量 (从文本描述估算)"""
        # TODO: 实现质量估算
        # "睡得很好" -> 8-10
        # "睡得一般" -> 5-7
        # "失眠" -> 1-4
        pass


# 测试用例
TEST_CASES = [
    {
        'input': '昨晚睡了8小时',
        'expected': {'intent': 'record_sleep', 'duration': 8.0}
    },
    {
        'input': '记录睡眠: 11点睡，6点起',
        'expected': {'intent': 'record_sleep', 'bedtime': '23:00', 'wakeup': '06:00'}
    },
    {
        'input': '失眠了，只睡了3小时',
        'expected': {'intent': 'record_sleep', 'duration': 3.0, 'quality': 2}
    },
]


def run_tests():
    """运行测试"""
    recognizer = SleepIntentRecognizer()
    
    for case in TEST_CASES:
        result = recognizer.recognize(case['input'])
        print(f"输入: {case['input']}")
        print(f"预期: {case['expected']}")
        print(f"实际: {result}")
        print()


if __name__ == '__main__':
    run_tests()
```

---

## 第三阶段：系统优化 (Day 6-7)

### 3.1 性能优化技巧

#### 缓存策略

```python
from functools import lru_cache
import time

class CachedHealthService:
    """带缓存的健康服务"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300  # 5分钟
    
    def get_stats(self, user_id: str, days: int = 7) -> dict:
        """获取统计（带缓存）"""
        cache_key = f"{user_id}_{days}"
        
        # 检查缓存
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
        
        # 从数据库获取
        data = self._calculate_stats(user_id, days)
        
        # 更新缓存
        self.cache[cache_key] = (data, time.time())
        
        return data
    
    @lru_cache(maxsize=128)
    def get_trend_cached(self, user_id: str, metric: str, days: int = 30):
        """使用 LRU 缓存的趋势查询"""
        return self._calculate_trend(user_id, metric, days)
```

#### 异步处理

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncHealthProcessor:
    """异步健康数据处理器"""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def generate_report_async(self, user_id: str) -> str:
        """异步生成报告"""
        loop = asyncio.get_event_loop()
        
        # 并行执行多个查询
        tasks = [
            loop.run_in_executor(self.executor, self._get_weight_data, user_id),
            loop.run_in_executor(self.executor, self._get_sleep_data, user_id),
            loop.run_in_executor(self.executor, self._get_exercise_data, user_id),
        ]
        
        weight_data, sleep_data, exercise_data = await asyncio.gather(*tasks)
        
        # 合并生成报告
        return self._compile_report(weight_data, sleep_data, exercise_data)
```

### 3.2 错误处理最佳实践

```python
from typing import Optional, Callable
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class HealthAssistantError(Exception):
    """健康助理基础异常"""
    pass


class DataValidationError(HealthAssistantError):
    """数据验证错误"""
    pass


class StorageError(HealthAssistantError):
    """存储错误"""
    pass


def handle_errors(fallback_message: str = "操作失败"):
    """错误处理装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except DataValidationError as e:
                logger.warning(f"Validation error: {e}")
                return f"❌ 数据错误: {str(e)}"
            except StorageError as e:
                logger.error(f"Storage error: {e}")
                return f"❌ 存储错误，请稍后重试"
            except Exception as e:
                logger.exception(f"Unexpected error: {e}")
                return f"❌ {fallback_message}"
        return wrapper
    return decorator


class HealthService:
    """健康服务类"""
    
    @handle_errors("记录失败")
    def record_weight(self, user_id: str, value: float) -> str:
        """记录体重"""
        # 验证
        if value <= 0 or value > 500:
            raise DataValidationError("体重必须在 0-500kg 之间")
        
        # 存储
        try:
            self.repository.save(user_id, 'weight', value)
        except Exception as e:
            raise StorageError(f"保存失败: {e}")
        
        return f"✅ 已记录体重 {value}kg"
```

---

## 第四阶段：项目实战 (Day 8-10)

### 4.1 完整项目架构

```
nanobot-health-assistant/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── agent.py          # Agent 核心
│   │   ├── intent.py         # 意图识别
│   │   └── response.py       # 响应生成
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── health.py         # 数据模型
│   │   └── entities.py       # 实体定义
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py           # Repository 基类
│   │   ├── health.py         # 健康数据仓库
│   │   └── sleep.py          # 睡眠数据仓库
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── health.py         # 健康服务
│   │   ├── analysis.py       # 分析服务
│   │   └── visualization.py  # 可视化服务
│   │
│   ├── skills/
│   │   ├── __init__.py
│   │   ├── weight/
│   │   │   └── SKILL.md
│   │   ├── sleep/
│   │   │   └── SKILL.md
│   │   └── ...
│   │
│   └── utils/
│       ├── __init__.py
│       ├── cache.py          # 缓存工具
│       ├── logger.py         # 日志工具
│       └── validators.py     # 验证工具
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_repositories.py
│   │   └── test_services.py
│   ├── integration/
│   │   └── test_workflows.py
│   └── fixtures/
│       └── test_data.json
│
├── docs/
│   ├── architecture/
│   ├── development/
│   ├── api/
│   └── deployment/
│
├── config/
│   └── nanobot.config.json
│
├── scripts/
│   ├── deploy.sh
│   └── backup.sh
│
├── requirements.txt
├── setup.py
├── README.md
├── CHANGELOG.md
└── LICENSE
```

### 4.2 代码审查清单

#### 代码质量
- [ ] 遵循 PEP 8 规范
- [ ] 使用类型提示
- [ ] 函数长度 < 50 行
- [ ] 类长度 < 300 行
- [ ] 圈复杂度 < 10

#### 测试覆盖
- [ ] 单元测试覆盖率 > 80%
- [ ] 集成测试覆盖核心流程
- [ ] 边界条件测试
- [ ] 错误处理测试

#### 文档
- [ ] 所有公共函数有文档字符串
- [ ] 复杂逻辑有注释
- [ ] README 包含使用示例
- [ ] CHANGELOG 记录变更

#### 性能
- [ ] 无明显性能瓶颈
- [ ] 适当使用缓存
- [ ] 数据库查询优化

---

## 第五阶段：持续学习

### 5.1 推荐阅读

1. **《设计数据密集型应用》** - Martin Kleppmann
2. **《构建机器学习系统》** - Chip Huyen
3. **《Clean Code》** - Robert C. Martin
4. **《Python 架构模式》** - Harry Percival

### 5.2 进阶方向

- **NLP 进阶**: 学习 Transformers、BERT 等模型
- **系统设计**: 学习分布式系统、微服务
- **MLOps**: 学习模型部署、监控、A/B 测试
- **数据工程**: 学习数据管道、ETL、数据仓库

### 5.3 开源贡献

- 参与 NanoBot 项目贡献
- 提交 bug 修复和功能改进
- 编写技术博客分享经验

---

## 培训总结

通过本培训，你应该掌握：

1. ✅ AI Agent 架构设计
2. ✅ NLP 意图识别和实体抽取
3. ✅ Repository 设计模式
4. ✅ 测试驱动开发
5. ✅ 性能优化技巧
6. ✅ 生产环境部署

**下一步**: 开始你的下一个 AI 项目！

---

*培训版本: 1.0.0*  
*作者: Chief AI Architect*  
*日期: 2026-03-15*
