# 开发指南 - 从零构建 AI 健康助理

## 1. 开发环境搭建

### 1.1 系统要求

```bash
# 基础环境
- Python 3.8+
- Git
- curl
- 2GB+ RAM
- 10GB+ 磁盘空间
```

### 1.2 环境初始化

```bash
# Step 1: 创建工作目录
mkdir -p ~/projects/nanobot-health
cd ~/projects/nanobot-health

# Step 2: 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# Step 3: 安装 NanoBot
pip install nanobot

# Step 4: 验证安装
nanobot --version
```

### 1.3 项目结构初始化

```bash
# 创建标准目录结构
mkdir -p skills/{health_data,diet_tracker,exercise_log,symptom_tracker,health_reminder,sleep_analyzer,step_tracker}
mkdir -p config
mkdir -p docs/{architecture,development,api,deployment,training}
mkdir -p tests
mkdir -p reports
```

---

## 2. 核心模块开发

### 2.1 数据管理层 (health_data_manager.py)

**设计原则**: Repository 模式 + 单例模式

```python
"""
健康数据管理模块
采用 Repository 设计模式，提供统一的数据访问接口
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union
from functools import lru_cache


# ==================== 配置 ====================
DATA_DIR = Path.home() / ".nanobot" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 数据文件路径
HEALTH_FILE = DATA_DIR / "health_metrics.json"
DIET_FILE = DATA_DIR / "diet_logs.json"
EXERCISE_FILE = DATA_DIR / "exercise_logs.json"
SYMPTOM_FILE = DATA_DIR / "symptom_logs.json"
REMINDER_FILE = DATA_DIR / "health_reminders.json"
SLEEP_FILE = DATA_DIR / "sleep_logs.json"
STEP_FILE = DATA_DIR / "step_logs.json"


# ==================== 工具函数 ====================
def init_data_files():
    """初始化所有数据文件"""
    files = [HEALTH_FILE, DIET_FILE, EXERCISE_FILE, 
             SYMPTOM_FILE, REMINDER_FILE, SLEEP_FILE, STEP_FILE]
    for file_path in files:
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)


def load_data(file_path: Path) -> dict:
    """加载 JSON 数据，带错误处理"""
    try:
        if not file_path.exists():
            return {}
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # 文件损坏，返回空数据
        return {}
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}


def save_data(file_path: Path, data: dict) -> bool:
    """保存 JSON 数据，原子操作"""
    try:
        # 先写入临时文件
        temp_file = file_path.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 原子重命名
        temp_file.replace(file_path)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False


# ==================== Repository 基类 ====================
class BaseRepository:
    """数据仓库基类"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._cache = None
        self._cache_timestamp = None
    
    def _get_data(self) -> dict:
        """获取数据，带缓存"""
        # 简单缓存策略：每次重新加载（适合小数据量）
        # 未来可优化为 LRU 缓存
        return load_data(self.file_path)
    
    def _save_data(self, data: dict) -> bool:
        """保存数据"""
        return save_data(self.file_path, data)


# ==================== 健康指标 Repository ====================
class HealthRepository(BaseRepository):
    """健康指标数据仓库"""
    
    def __init__(self):
        super().__init__(HEALTH_FILE)
    
    def record(self, metric_type: str, value: Union[float, int], 
               unit: str, note: str = "") -> dict:
        """记录健康指标"""
        data = self._get_data()
        
        if metric_type not in data:
            data[metric_type] = []
        
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "value": value,
            "unit": unit,
            "note": note
        }
        
        data[metric_type].append(entry)
        self._save_data(data)
        return entry
    
    def get_recent(self, metric_type: str, days: int = 7) -> List[dict]:
        """获取最近的健康指标"""
        data = self._get_data()
        if metric_type not in data:
            return []
        
        cutoff_date = datetime.now() - timedelta(days=days)
        return [
            entry for entry in data[metric_type]
            if datetime.strptime(entry["date"], "%Y-%m-%d") >= cutoff_date
        ]
    
    def get_trend(self, metric_type: str, days: int = 30) -> dict:
        """获取趋势分析"""
        records = self.get_recent(metric_type, days)
        if not records:
            return {}
        
        values = [r["value"] for r in records]
        return {
            "count": len(values),
            "start": values[0] if values else None,
            "end": values[-1] if values else None,
            "min": min(values) if values else None,
            "max": max(values) if values else None,
            "avg": sum(values) / len(values) if values else None,
            "change": values[-1] - values[0] if len(values) > 1 else 0
        }


# ==================== 睡眠 Repository ====================
class SleepRepository(BaseRepository):
    """睡眠数据仓库"""
    
    def __init__(self):
        super().__init__(SLEEP_FILE)
    
    def record(self, duration: float, quality_score: int, 
               bedtime: str, wakeup_time: str, **kwargs) -> dict:
        """记录睡眠"""
        data = self._get_data()
        
        if "sleep_logs" not in data:
            data["sleep_logs"] = []
        
        # 质量评分映射
        quality_map = {
            9: "excellent", 10: "excellent",
            7: "good", 8: "good",
            5: "fair", 6: "fair",
            3: "poor", 4: "poor",
            1: "very_poor", 2: "very_poor"
        }
        
        entry = {
            "id": f"sleep_{len(data['sleep_logs']) + 1:03d}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "bedtime": bedtime,
            "wakeup_time": wakeup_time,
            "duration": duration,
            "quality": quality_map.get(quality_score, "fair"),
            "quality_score": quality_score,
            "sleep_onset_minutes": kwargs.get("sleep_onset_minutes", 0),
            "awakenings": kwargs.get("awakenings", 0),
            "factors": kwargs.get("factors", {}),
            "notes": kwargs.get("notes", "")
        }
        
        data["sleep_logs"].append(entry)
        self._save_data(data)
        return entry
    
    def get_stats(self, days: int = 7) -> dict:
        """获取睡眠统计"""
        data = self._get_data()
        logs = data.get("sleep_logs", [])
        
        if not logs:
            return {}
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_logs = [
            log for log in logs
            if datetime.strptime(log["date"], "%Y-%m-%d") >= cutoff_date
        ]
        
        if not recent_logs:
            return {}
        
        durations = [log["duration"] for log in recent_logs]
        scores = [log["quality_score"] for log in recent_logs]
        
        return {
            "avg_duration": round(sum(durations) / len(durations), 1),
            "avg_quality": round(sum(scores) / len(scores), 1),
            "total_logs": len(recent_logs),
            "best_night": max(recent_logs, key=lambda x: x["quality_score"]),
            "worst_night": min(recent_logs, key=lambda x: x["quality_score"]),
            "logs": recent_logs
        }


# 类似实现其他 Repository...
# DietRepository, ExerciseRepository, StepRepository, SymptomRepository


# ==================== 统一入口 ====================
class HealthDataManager:
    """
    健康数据管理器
    提供统一的数据访问接口
    """
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_repositories()
        return cls._instance
    
    def _init_repositories(self):
        """初始化所有仓库"""
        self.repositories = {
            'health': HealthRepository(),
            'sleep': SleepRepository(),
            # 'diet': DietRepository(),
            # 'exercise': ExerciseRepository(),
            # 'step': StepRepository(),
            # 'symptom': SymptomRepository(),
        }
    
    def record(self, domain: str, **kwargs):
        """统一记录接口"""
        if domain not in self.repositories:
            raise ValueError(f"Unknown domain: {domain}")
        return self.repositories[domain].record(**kwargs)
    
    def get_stats(self, domain: str, days: int = 7):
        """统一统计接口"""
        if domain not in self.repositories:
            raise ValueError(f"Unknown domain: {domain}")
        repo = self.repositories[domain]
        if hasattr(repo, 'get_stats'):
            return repo.get_stats(days)
        return {}


# 初始化
init_data_files()

# 使用示例
if __name__ == "__main__":
    manager = HealthDataManager()
    
    # 记录体重
    manager.record('health', metric_type='weight', value=70.5, unit='kg')
    
    # 记录睡眠
    manager.record('sleep', duration=7.5, quality_score=8, 
                   bedtime='23:00', wakeup_time='06:30')
    
    # 获取统计
    print(manager.get_stats('sleep', days=7))
```

### 2.2 技能定义 (SKILL.md)

每个技能必须包含 SKILL.md 文件：

```markdown
---
name: skill-name
description: 技能描述
version: 1.0.0
author: Your Name
tags: [health, tracking]
---

# 技能名称

## 功能概述

简要描述技能的功能。

## 使用示例

- "记录体重 70kg"
- "查看最近一周的体重变化"

## 数据结构

```json
{
  "field": "type",
  "description": "说明"
}
```

## 注意事项

- 注意事项 1
- 注意事项 2
```

---

## 3. 意图识别设计

### 3.1 意图分类

```python
# 意图定义
class IntentType:
    # 数据记录类
    RECORD_WEIGHT = "record_weight"
    RECORD_SLEEP = "record_sleep"
    RECORD_EXERCISE = "record_exercise"
    
    # 查询类
    QUERY_STATS = "query_stats"
    QUERY_TREND = "query_trend"
    QUERY_REPORT = "query_report"
    
    # 分析类
    ANALYZE_SLEEP = "analyze_sleep"
    ANALYZE_DIET = "analyze_diet"
    
    # 设置类
    SET_GOAL = "set_goal"
    SET_REMINDER = "set_reminder"
    
    # 其他
    GREETING = "greeting"
    HELP = "help"
    UNKNOWN = "unknown"


# 意图识别规则（基于关键词）
INTENT_PATTERNS = {
    IntentType.RECORD_WEIGHT: [
        r"记录.*体重",
        r"体重.*(\d+)",
        r"称重",
    ],
    IntentType.RECORD_SLEEP: [
        r"记录.*睡眠",
        r"睡了.*(\d+)小时",
        r"昨晚.*睡眠",
    ],
    # ... 更多规则
}
```

### 3.2 实体抽取

```python
import re
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Entity:
    type: str
    value: any
    start: int
    end: int


class EntityExtractor:
    """实体抽取器"""
    
    # 实体模式
    PATTERNS = {
        'weight': r'(\d+\.?\d*)\s*(kg|公斤|千克)',
        'duration': r'(\d+\.?\d*)\s*(小时|h|分钟|min)',
        'time': r'(\d{1,2}):(\d{2})',
        'date': r'(\d{4})-(\d{2})-(\d{2})',
        'calories': r'(\d+)\s*(卡|卡路里|kcal)',
        'steps': r'(\d+)\s*(步|步数)',
    }
    
    def extract(self, text: str) -> List[Entity]:
        """从文本中抽取实体"""
        entities = []
        
        for entity_type, pattern in self.PATTERNS.items():
            for match in re.finditer(pattern, text):
                entity = Entity(
                    type=entity_type,
                    value=match.group(1),
                    start=match.start(),
                    end=match.end()
                )
                entities.append(entity)
        
        return entities


# 使用示例
extractor = EntityExtractor()
entities = extractor.extract("我体重 70.5kg，昨天走了 8500 步")
# 结果: [Entity(type='weight', value='70.5', ...), Entity(type='steps', value='8500', ...)]
```

---

## 4. 响应生成

### 4.1 模板引擎

```python
from string import Template

class ResponseTemplate:
    """响应模板"""
    
    TEMPLATES = {
        'record_success': Template(
            "✅ 已记录！$what $value$unit"
        ),
        'trend_up': Template(
            "📈 $what 呈上升趋势，从 $start 到 $end（+$change）"
        ),
        'trend_down': Template(
            "📉 $what 呈下降趋势，从 $start 到 $end（$change）"
        ),
        'goal_reached': Template(
            "🎉 恭喜！你达成了 $goal 目标！"
        ),
        'goal_missed': Template(
            "💪 加油！离 $goal 目标还差 $remaining"
        ),
    }
    
    @classmethod
    def render(cls, template_name: str, **kwargs) -> str:
        """渲染模板"""
        template = cls.TEMPLATES.get(template_name)
        if template:
            return template.safe_substitute(**kwargs)
        return ""


# 使用示例
response = ResponseTemplate.render(
    'record_success',
    what='体重',
    value=70.5,
    unit='kg'
)
# 结果: "✅ 已记录！体重 70.5kg"
```

---

## 5. 测试驱动开发 (TDD)

### 5.1 单元测试

```python
import unittest
from unittest.mock import patch, MagicMock

class TestHealthRepository(unittest.TestCase):
    """健康数据仓库测试"""
    
    def setUp(self):
        """测试前准备"""
        self.repo = HealthRepository()
        # 使用临时文件
        self.repo.file_path = Path("/tmp/test_health.json")
    
    def tearDown(self):
        """测试后清理"""
        if self.repo.file_path.exists():
            self.repo.file_path.unlink()
    
    def test_record_weight(self):
        """测试记录体重"""
        entry = self.repo.record('weight', 70.5, 'kg', '早餐前')
        
        self.assertEqual(entry['value'], 70.5)
        self.assertEqual(entry['unit'], 'kg')
        self.assertIn('date', entry)
        self.assertIn('time', entry)
    
    def test_get_recent(self):
        """测试获取最近记录"""
        # 插入测试数据
        self.repo.record('weight', 70.0, 'kg')
        self.repo.record('weight', 70.5, 'kg')
        
        # 获取最近记录
        records = self.repo.get_recent('weight', days=7)
        
        self.assertEqual(len(records), 2)
        self.assertEqual(records[-1]['value'], 70.5)
    
    def test_get_trend(self):
        """测试趋势分析"""
        self.repo.record('weight', 72.0, 'kg')
        self.repo.record('weight', 71.5, 'kg')
        self.repo.record('weight', 70.5, 'kg')
        
        trend = self.repo.get_trend('weight', days=7)
        
        self.assertEqual(trend['start'], 72.0)
        self.assertEqual(trend['end'], 70.5)
        self.assertEqual(trend['change'], -1.5)


class TestEntityExtractor(unittest.TestCase):
    """实体抽取测试"""
    
    def setUp(self):
        self.extractor = EntityExtractor()
    
    def test_extract_weight(self):
        """测试体重抽取"""
        entities = self.extractor.extract("我体重 70.5kg")
        
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].type, 'weight')
        self.assertEqual(entities[0].value, '70.5')
    
    def test_extract_multiple(self):
        """测试多实体抽取"""
        entities = self.extractor.extract("体重 70kg，走了 8000 步")
        
        self.assertEqual(len(entities), 2)
        types = [e.type for e in entities]
        self.assertIn('weight', types)
        self.assertIn('steps', types)


if __name__ == '__main__':
    unittest.main()
```

### 5.2 集成测试

```python
class TestHealthAssistantIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流程"""
        # 1. 记录体重
        # 2. 记录运动
        # 3. 生成报告
        # 验证数据一致性
        pass
    
    def test_data_persistence(self):
        """测试数据持久化"""
        # 写入数据
        # 重启服务
        # 验证数据仍在
        pass
```

---

## 6. 性能优化

### 6.1 缓存策略

```python
from functools import lru_cache
import time

class CachedRepository:
    """带缓存的数据仓库"""
    
    def __init__(self, repo, cache_ttl=60):
        self.repo = repo
        self.cache = {}
        self.cache_time = {}
        self.cache_ttl = cache_ttl
    
    def get(self, key):
        """带缓存的获取"""
        now = time.time()
        
        # 检查缓存是否有效
        if key in self.cache:
            if now - self.cache_time[key] < self.cache_ttl:
                return self.cache[key]
        
        # 从源获取
        value = self.repo.get(key)
        
        # 更新缓存
        self.cache[key] = value
        self.cache_time[key] = now
        
        return value
    
    def invalidate(self, key=None):
        """使缓存失效"""
        if key:
            self.cache.pop(key, None)
            self.cache_time.pop(key, None)
        else:
            self.cache.clear()
            self.cache_time.clear()
```

### 6.2 异步处理

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncHealthProcessor:
    """异步健康数据处理器"""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def process_batch(self, records):
        """批量异步处理"""
        loop = asyncio.get_event_loop()
        
        # 提交多个任务
        tasks = [
            loop.run_in_executor(
                self.executor, 
                self._process_single, 
                record
            )
            for record in records
        ]
        
        # 等待所有完成
        results = await asyncio.gather(*tasks)
        return results
    
    def _process_single(self, record):
        """处理单条记录"""
        # 耗时操作
        pass
```

---

## 7. 错误处理

### 7.1 异常层次

```python
class HealthAssistantException(Exception):
    """基础异常"""
    pass

class DataValidationError(HealthAssistantException):
    """数据验证错误"""
    pass

class StorageError(HealthAssistantException):
    """存储错误"""
    pass

class SkillNotFoundError(HealthAssistantException):
    """技能未找到"""
    pass


# 错误处理装饰器
def handle_errors(func):
    """错误处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DataValidationError as e:
            return f"❌ 数据错误: {str(e)}"
        except StorageError as e:
            return f"❌ 存储错误: {str(e)}"
        except Exception as e:
            return f"❌ 系统错误: {str(e)}"
    return wrapper
```

---

## 8. 日志记录

```python
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('health_assistant.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('health_assistant')


class HealthLogger:
    """健康助理日志器"""
    
    @staticmethod
    def log_record(user_id: str, record_type: str, data: dict):
        """记录数据操作"""
        logger.info(
            f"Record created - User: {user_id}, "
            f"Type: {record_type}, Data: {data}"
        )
    
    @staticmethod
    def log_query(user_id: str, query_type: str, params: dict):
        """记录查询操作"""
        logger.info(
            f"Query executed - User: {user_id}, "
            f"Type: {query_type}, Params: {params}"
        )
    
    @staticmethod
    def log_error(user_id: str, error: Exception, context: dict):
        """记录错误"""
        logger.error(
            f"Error occurred - User: {user_id}, "
            f"Error: {str(error)}, Context: {context}",
            exc_info=True
        )
```

---

## 9. 持续集成

### 9.1 GitHub Actions 配置

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## 10. 总结

开发 NanoBot 健康助理的关键步骤：

1. **设计优先** - 先设计架构和数据模型
2. **模块开发** - 按技能独立开发
3. **测试驱动** - 先写测试再写实现
4. **文档同步** - 代码和文档同步更新
5. **持续集成** - 自动化测试和部署

---

*文档版本: 1.0.0*  
*作者: Chief AI Architect*  
*日期: 2026-03-15*
