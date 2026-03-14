# API 文档 - NanoBot 健康助理

## 1. 核心模块 API

### 1.1 HealthDataManager

```python
class HealthDataManager:
    """
    健康数据管理器 - 统一数据访问接口
    
    采用单例模式，全局唯一实例
    """
    
    # 获取实例
    manager = HealthDataManager()
```

#### 方法列表

##### `record(domain: str, **kwargs) -> dict`
记录健康数据

**参数:**
- `domain` (str): 数据域，可选值: 'health', 'sleep', 'diet', 'exercise', 'step', 'symptom'
- `**kwargs`: 根据 domain 不同而变化

**返回值:**
- `dict`: 记录的数据条目

**示例:**
```python
# 记录体重
manager.record('health', 
    metric_type='weight', 
    value=70.5, 
    unit='kg',
    note='早餐前'
)

# 记录睡眠
manager.record('sleep',
    duration=7.5,
    quality_score=8,
    bedtime='23:00',
    wakeup_time='06:30'
)
```

---

##### `get_stats(domain: str, days: int = 7) -> dict`
获取统计数据

**参数:**
- `domain` (str): 数据域
- `days` (int): 查询天数，默认 7 天

**返回值:**
- `dict`: 统计数据

**示例:**
```python
# 获取最近 7 天睡眠统计
stats = manager.get_stats('sleep', days=7)
# 返回: {
#     'avg_duration': 7.5,
#     'avg_quality': 8.0,
#     'total_logs': 7,
#     ...
# }
```

---

### 1.2 HealthRepository

```python
class HealthRepository(BaseRepository):
    """
    健康指标数据仓库
    管理体重、血压、心率等基础健康指标
    """
```

#### 方法列表

##### `record(metric_type: str, value: float, unit: str, note: str = "") -> dict`
记录健康指标

**参数:**
- `metric_type` (str): 指标类型，如 'weight', 'blood_pressure', 'heart_rate'
- `value` (float): 数值
- `unit` (str): 单位，如 'kg', 'mmHg', 'bpm'
- `note` (str, optional): 备注

**示例:**
```python
repo = HealthRepository()

# 记录体重
repo.record('weight', 70.5, 'kg', '早餐前')

# 记录血压 (收缩压/舒张压)
repo.record('blood_pressure', '120/80', 'mmHg')

# 记录心率
repo.record('heart_rate', 72, 'bpm', '静息状态')
```

---

##### `get_recent(metric_type: str, days: int = 7) -> List[dict]`
获取最近的记录

**返回值示例:**
```python
[
    {
        'date': '2026-03-15',
        'time': '08:00',
        'value': 70.5,
        'unit': 'kg',
        'note': '早餐前'
    },
    # ...
]
```

---

##### `get_trend(metric_type: str, days: int = 30) -> dict`
获取趋势分析

**返回值:**
```python
{
    'count': 10,          # 记录数量
    'start': 72.0,        # 起始值
    'end': 70.5,          # 结束值
    'min': 70.0,          # 最小值
    'max': 72.5,          # 最大值
    'avg': 71.2,          # 平均值
    'change': -1.5        # 变化量
}
```

---

### 1.3 SleepRepository

```python
class SleepRepository(BaseRepository):
    """
    睡眠数据仓库
    管理睡眠记录和分析
    """
```

#### 方法列表

##### `record(duration: float, quality_score: int, bedtime: str, wakeup_time: str, **kwargs) -> dict`
记录睡眠数据

**参数:**
- `duration` (float): 睡眠时长（小时）
- `quality_score` (int): 质量评分 1-10
- `bedtime` (str): 就寝时间，格式 "HH:MM"
- `wakeup_time` (str): 起床时间，格式 "HH:MM"
- `sleep_onset_minutes` (int, optional): 入睡时间（分钟）
- `awakenings` (int, optional): 觉醒次数
- `factors` (dict, optional): 影响因素
- `notes` (str, optional): 备注

**示例:**
```python
repo = SleepRepository()

repo.record(
    duration=7.5,
    quality_score=8,
    bedtime='23:00',
    wakeup_time='06:30',
    sleep_onset_minutes=15,
    awakenings=1,
    factors={
        'caffeine': False,
        'exercise': True,
        'screens': False
    },
    notes='睡得很香'
)
```

---

##### `get_stats(days: int = 7) -> dict`
获取睡眠统计

**返回值:**
```python
{
    'avg_duration': 7.5,        # 平均睡眠时长
    'avg_quality': 8.0,         # 平均质量评分
    'total_logs': 7,            # 记录数量
    'best_night': {...},        # 最佳睡眠记录
    'worst_night': {...},       # 最差睡眠记录
    'logs': [...]               # 详细记录列表
}
```

---

### 1.4 StepRepository

```python
class StepRepository(BaseRepository):
    """
    步数数据仓库
    管理步数记录和成就
    """
```

#### 方法列表

##### `record(steps: int, distance_km: float = None, active_minutes: int = None, calories: int = None, goal: int = 10000, notes: str = "") -> dict`
记录步数

**参数:**
- `steps` (int): 步数
- `distance_km` (float, optional): 距离（公里），自动估算
- `active_minutes` (int, optional): 活跃时间（分钟），自动估算
- `calories` (int, optional): 消耗卡路里，自动估算
- `goal` (int, optional): 目标步数，默认 10000
- `notes` (str, optional): 备注

**返回值:**
```python
{
    'date': '2026-03-15',
    'steps': 8500,
    'distance_km': 6.8,
    'active_minutes': 45,
    'calories': 340,
    'goal_reached': False,
    'goal_percentage': 85,
    'notes': '今天走路去上班'
}
```

---

## 2. 可视化模块 API

### 2.1 HealthVisualizer

```python
class HealthVisualizer:
    """
    健康数据可视化器
    生成图表和报告
    """
```

#### 构造函数

```python
viz = HealthVisualizer(output_dir: str = "reports")
```

**参数:**
- `output_dir` (str): 输出目录，默认 "reports"

---

#### 方法列表

##### `generate_weight_chart(days: int = 30, output_file: str = None) -> str`
生成体重趋势图

**参数:**
- `days` (int): 查询天数，默认 30 天
- `output_file` (str, optional): 输出文件路径

**返回值:**
- `str`: 生成的图表文件路径

**示例:**
```python
chart_path = viz.generate_weight_chart(days=30)
print(f"图表已生成: {chart_path}")
# 输出: 图表已生成: reports/weight_chart_20260315.png
```

---

##### `generate_sleep_chart(days: int = 14, output_file: str = None) -> str`
生成睡眠分析图

**功能:** 生成包含睡眠时长和质量评分的组合图表

---

##### `generate_steps_chart(days: int = 14, output_file: str = None) -> str`
生成步数统计图

**功能:** 生成步数柱状图，达标/未达标用不同颜色标注

---

##### `generate_weekly_report(output_file: str = None) -> str`
生成周报

**返回值:**
- `str`: 周报文本内容

**示例输出:**
```
==================================================
         本周健康报告
         2026年03月15日
==================================================

📊 步数统计
------------------------------
  平均步数: 8,500 步/天
  总步数: 59,500 步
  达标天数: 5/7 天

😴 睡眠统计
------------------------------
  平均睡眠: 7.2 小时/天
  平均质量: 7.8/10
  记录天数: 7 天

💪 运动统计
------------------------------
  总运动时长: 210 分钟
  消耗卡路里: 2100 kcal

==================================================
💡 健康建议
==================================================
  • 步数很棒！保持这个活跃水平
  • 睡眠质量良好，继续保持规律作息
==================================================
```

---

##### `generate_html_report(days: int = 7, output_file: str = None) -> str`
生成 HTML 报告

**功能:** 生成美观的网页版健康报告，包含:
- 响应式设计
- 数据卡片展示
- 健康建议
- 专业配色

**返回值:**
- `str`: HTML 文件路径

---

## 3. 实体抽取 API

### 3.1 EntityExtractor

```python
class EntityExtractor:
    """
    实体抽取器
    从自然语言中抽取结构化数据
    """
```

#### 方法列表

##### `extract(text: str) -> List[Entity]`
从文本中抽取实体

**参数:**
- `text` (str): 输入文本

**返回值:**
- `List[Entity]`: 实体列表

**支持的实体类型:**
- `weight` - 体重
- `duration` - 时长
- `time` - 时间
- `date` - 日期
- `calories` - 卡路里
- `steps` - 步数

**示例:**
```python
extractor = EntityExtractor()

entities = extractor.extract("我体重 70.5kg，昨天走了 8500 步，跑了 30 分钟")

for entity in entities:
    print(f"{entity.type}: {entity.value}")
    
# 输出:
# weight: 70.5
# steps: 8500
# duration: 30
```

---

## 4. 响应模板 API

### 4.1 ResponseTemplate

```python
class ResponseTemplate:
    """
    响应模板引擎
    生成格式化的回复消息
    """
```

#### 方法列表

##### `render(template_name: str, **kwargs) -> str`
渲染模板

**可用模板:**
- `record_success` - 记录成功
- `trend_up` - 上升趋势
- `trend_down` - 下降趋势
- `goal_reached` - 目标达成
- `goal_missed` - 未达目标

**示例:**
```python
# 记录成功
response = ResponseTemplate.render(
    'record_success',
    what='体重',
    value=70.5,
    unit='kg'
)
# 结果: "✅ 已记录！体重 70.5kg"

# 趋势下降
response = ResponseTemplate.render(
    'trend_down',
    what='体重',
    start=72.0,
    end=70.5,
    change='-1.5kg'
)
# 结果: "📉 体重 呈下降趋势，从 72.0 到 70.5（-1.5kg）"
```

---

## 5. 配置 API

### 5.1 配置文件结构

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["*"]
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-3.5-sonnet",
      "provider": "openrouter",
      "systemPrompt": "...",
      "skills": [
        "health_data",
        "diet_tracker",
        "exercise_log",
        "symptom_tracker",
        "health_reminder",
        "sleep_analyzer",
        "step_tracker"
      ]
    }
  },
  "cron": {
    "enabled": true,
    "jobs": [
      {
        "name": "morning_reminder",
        "schedule": "0 8 * * *",
        "message": "早上好！记得记录今天的健康数据~"
      }
    ]
  }
}
```

---

## 6. 错误代码

### 6.1 异常类型

| 异常 | 说明 | 处理方式 |
|------|------|---------|
| `DataValidationError` | 数据验证失败 | 检查输入格式 |
| `StorageError` | 存储错误 | 检查磁盘空间和权限 |
| `SkillNotFoundError` | 技能未找到 | 检查配置是否正确 |
| `EntityExtractionError` | 实体抽取失败 | 使用更清晰的表述 |

### 6.2 错误示例

```python
try:
    manager.record('health', metric_type='weight', value='invalid')
except DataValidationError as e:
    print(f"数据错误: {e}")
    # 输出: 数据错误: value must be a number
    
try:
    manager.get_stats('unknown_domain')
except SkillNotFoundError as e:
    print(f"技能错误: {e}")
    # 输出: 技能错误: Unknown domain: unknown_domain
```

---

## 7. 使用示例

### 7.1 完整工作流程

```python
from health_data_manager import HealthDataManager
from visualization import HealthVisualizer

# 1. 初始化
manager = HealthDataManager()
viz = HealthVisualizer()

# 2. 记录数据
# 记录体重
manager.record('health', 
    metric_type='weight', 
    value=70.5, 
    unit='kg'
)

# 记录睡眠
manager.record('sleep',
    duration=7.5,
    quality_score=8,
    bedtime='23:00',
    wakeup_time='06:30'
)

# 记录步数
manager.record('step',
    steps=8500,
    notes='今天走路去上班'
)

# 3. 获取统计
weight_trend = manager.repositories['health'].get_trend('weight', days=30)
sleep_stats = manager.get_stats('sleep', days=7)

# 4. 生成可视化
viz.generate_weight_chart(days=30)
viz.generate_sleep_chart(days=14)

# 5. 生成报告
report = viz.generate_weekly_report()
html_report = viz.generate_html_report(days=7)

print("健康数据管理完成！")
```

---

## 8. 扩展 API

### 8.1 添加自定义技能

```python
# 1. 创建技能类
class CustomSkill:
    def __init__(self):
        self.repository = CustomRepository()
    
    def handle(self, intent, context):
        """处理意图"""
        pass

# 2. 注册技能
SKILL_REGISTRY = {
    'health_data': HealthSkill(),
    'custom_skill': CustomSkill(),  # 新增
}

# 3. 更新配置
# config/nanobot.config.json
{
  "skills": [
    "health_data",
    "custom_skill"  # 新增
  ]
}
```

---

*文档版本: 1.0.0*  
*作者: Chief AI Architect*  
*日期: 2026-03-15*
