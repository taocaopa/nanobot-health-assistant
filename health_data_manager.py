#!/usr/bin/env python3
"""
健康数据管理模块
用于 NanoBot 健康助理的数据存储和查询
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path.home() / ".nanobot" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

HEALTH_FILE = DATA_DIR / "health_metrics.json"
DIET_FILE = DATA_DIR / "diet_logs.json"
EXERCISE_FILE = DATA_DIR / "exercise_logs.json"
SYMPTOM_FILE = DATA_DIR / "symptom_logs.json"
REMINDER_FILE = DATA_DIR / "health_reminders.json"
SLEEP_FILE = DATA_DIR / "sleep_logs.json"
STEP_FILE = DATA_DIR / "step_logs.json"


def init_data_files():
    """初始化数据文件"""
    for file_path in [HEALTH_FILE, DIET_FILE, EXERCISE_FILE, SYMPTOM_FILE, 
                      REMINDER_FILE, SLEEP_FILE, STEP_FILE]:
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)


def load_data(file_path):
    """加载 JSON 数据"""
    if not file_path.exists():
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(file_path, data):
    """保存 JSON 数据"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ========== 健康数据 ==========
def record_health_metric(metric_type, value, unit, note=""):
    """记录健康指标"""
    data = load_data(HEALTH_FILE)
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
    save_data(HEALTH_FILE, data)
    return entry


def get_health_metrics(metric_type, days=7):
    """获取最近的健康指标"""
    data = load_data(HEALTH_FILE)
    if metric_type not in data:
        return []
    
    cutoff_date = datetime.now() - timedelta(days=days)
    return [
        entry for entry in data[metric_type]
        if datetime.strptime(entry["date"], "%Y-%m-%d") >= cutoff_date
    ]


# ========== 饮食记录 ==========
def record_meal(meal_type, items, calories=None, note=""):
    """记录饮食"""
    data = load_data(DIET_FILE)
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in data:
        data[today] = {"meals": [], "total_calories": 0, "water_intake": 0}
    
    meal = {
        "type": meal_type,
        "time": datetime.now().strftime("%H:%M"),
        "items": items if isinstance(items, list) else [items],
        "calories": calories or estimate_calories(items),
        "note": note
    }
    data[today]["meals"].append(meal)
    data[today]["total_calories"] = sum(m.get("calories", 0) for m in data[today]["meals"])
    
    save_data(DIET_FILE, data)
    return meal


def estimate_calories(items):
    """简单估算卡路里"""
    calorie_table = {
        "米饭": 174, "粥": 60, "面条": 280, "面包": 265,
        "鸡蛋": 70, "牛奶": 150, "豆浆": 45,
        "苹果": 100, "香蕉": 90, "橙子": 60,
        "鸡胸肉": 165, "牛肉": 250, "猪肉": 280,
        "鱼": 200, "虾": 85, "豆腐": 80,
        "青菜": 25, "西兰花": 35, "番茄": 20,
        "咖啡": 5, "茶": 2, "果汁": 120
    }
    
    total = 0
    items_list = items if isinstance(items, list) else [items]
    for item in items_list:
        for food, cal in calorie_table.items():
            if food in item:
                total += cal
                break
    return total


# ========== 运动记录 ==========
def record_exercise(exercise_type, duration, calories=None, note=""):
    """记录运动"""
    data = load_data(EXERCISE_FILE)
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in data:
        data[today] = {"activities": [], "total_duration": 0, "total_calories": 0}
    
    calories = calories or estimate_exercise_calories(exercise_type, duration)
    activity = {
        "type": exercise_type,
        "duration": duration,
        "unit": "minutes",
        "calories": calories,
        "time": datetime.now().strftime("%H:%M"),
        "note": note
    }
    data[today]["activities"].append(activity)
    data[today]["total_duration"] += duration
    data[today]["total_calories"] += calories
    
    save_data(EXERCISE_FILE, data)
    return activity


def estimate_exercise_calories(exercise_type, duration):
    """估算运动消耗"""
    burn_rate = {
        "跑步": 10, "慢跑": 8, "快走": 5, "散步": 3,
        "游泳": 8, "骑车": 6, "骑行": 6, "瑜伽": 4,
        "健身": 6, "力量训练": 6, "跳绳": 12,
        "羽毛球": 7, "篮球": 8, "足球": 9
    }
    rate = burn_rate.get(exercise_type, 5)
    return rate * duration


# ========== 症状记录 ==========
def record_symptom(symptom, severity, duration="", triggers=None, notes=""):
    """记录症状"""
    data = load_data(SYMPTOM_FILE)
    
    if "symptoms" not in data:
        data["symptoms"] = []
    
    entry = {
        "id": f"sym_{len(data['symptoms']) + 1:03d}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "symptom": symptom,
        "severity": severity,
        "duration": duration,
        "triggers": triggers or [],
        "notes": notes
    }
    data["symptoms"].append(entry)
    save_data(SYMPTOM_FILE, data)
    return entry


# ========== 睡眠记录 ==========
def record_sleep(duration, quality_score, bedtime, wakeup_time, sleep_onset_minutes=0, 
                 awakenings=0, factors=None, notes=""):
    """记录睡眠数据"""
    data = load_data(SLEEP_FILE)
    
    if "sleep_logs" not in data:
        data["sleep_logs"] = []
    
    quality_map = {9: "excellent", 8: "good", 7: "good", 6: "fair", 5: "fair", 
                   4: "poor", 3: "poor", 2: "very_poor", 1: "very_poor"}
    quality = quality_map.get(quality_score, "fair")
    
    entry = {
        "id": f"sleep_{len(data['sleep_logs']) + 1:03d}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "bedtime": bedtime,
        "wakeup_time": wakeup_time,
        "duration": duration,
        "quality": quality,
        "quality_score": quality_score,
        "sleep_onset_minutes": sleep_onset_minutes,
        "awakenings": awakenings,
        "factors": factors or {},
        "notes": notes
    }
    data["sleep_logs"].append(entry)
    save_data(SLEEP_FILE, data)
    return entry


def get_sleep_stats(days=7):
    """获取睡眠统计"""
    data = load_data(SLEEP_FILE)
    if "sleep_logs" not in data:
        return {}
    
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_logs = [
        log for log in data["sleep_logs"]
        if datetime.strptime(log["date"], "%Y-%m-%d") >= cutoff_date
    ]
    
    if not recent_logs:
        return {}
    
    durations = [log["duration"] for log in recent_logs]
    scores = [log["quality_score"] for log in recent_logs]
    
    return {
        "avg_duration": sum(durations) / len(durations),
        "avg_quality": sum(scores) / len(scores),
        "total_logs": len(recent_logs),
        "best_sleep": max(recent_logs, key=lambda x: x["quality_score"]),
        "logs": recent_logs
    }


def set_sleep_goal(target_duration, target_bedtime, target_wakeup):
    """设置睡眠目标"""
    data = load_data(SLEEP_FILE)
    data["sleep_goals"] = {
        "target_duration": target_duration,
        "target_bedtime": target_bedtime,
        "target_wakeup": target_wakeup
    }
    save_data(SLEEP_FILE, data)
    return data["sleep_goals"]


# ========== 步数记录 ==========
def record_steps(steps, distance_km=None, active_minutes=None, calories=None, 
                 goal=10000, notes=""):
    """记录步数"""
    data = load_data(STEP_FILE)
    
    if "daily_steps" not in data:
        data["daily_steps"] = []
    
    # 估算距离和卡路里
    if distance_km is None:
        distance_km = steps * 0.0007  # 平均步幅
    if calories is None:
        calories = steps * 0.04  # 每步约0.04卡
    if active_minutes is None:
        active_minutes = steps // 100  # 估算
    
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "steps": steps,
        "distance_km": round(distance_km, 2),
        "active_minutes": active_minutes,
        "calories": int(calories),
        "goal_reached": steps >= goal,
        "goal_percentage": min(100, int(steps / goal * 100)),
        "manual_entry": True,
        "source": "user_input",
        "notes": notes
    }
    data["daily_steps"].append(entry)
    
    # 更新统计
    update_step_statistics(data)
    save_data(STEP_FILE, data)
    return entry


def update_step_statistics(data):
    """更新步数统计"""
    if "daily_steps" not in data or not data["daily_steps"]:
        return
    
    steps_list = data["daily_steps"]
    recent_7_days = steps_list[-7:] if len(steps_list) >= 7 else steps_list
    
    # 计算连续达标天数
    current_streak = 0
    for log in reversed(steps_list):
        if log.get("goal_reached", False):
            current_streak += 1
        else:
            break
    
    # 计算最长连续
    longest_streak = 0
    temp_streak = 0
    for log in steps_list:
        if log.get("goal_reached", False):
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 0
    
    data["statistics"] = {
        "avg_daily_steps": sum(s["steps"] for s in steps_list) // len(steps_list),
        "best_day": max(steps_list, key=lambda x: x["steps"]),
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_steps_this_month": sum(s["steps"] for s in steps_list 
                                      if s["date"].startswith(datetime.now().strftime("%Y-%m")))
    }


def get_step_stats(days=7):
    """获取步数统计"""
    data = load_data(STEP_FILE)
    if "daily_steps" not in data:
        return {}
    
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_logs = [
        log for log in data["daily_steps"]
        if datetime.strptime(log["date"], "%Y-%m-%d") >= cutoff_date
    ]
    
    if not recent_logs:
        return {}
    
    return {
        "avg_steps": sum(log["steps"] for log in recent_logs) // len(recent_logs),
        "total_steps": sum(log["steps"] for log in recent_logs),
        "goal_reached_days": sum(1 for log in recent_logs if log.get("goal_reached", False)),
        "total_days": len(recent_logs),
        "logs": recent_logs
    }


def set_step_goal(daily_steps, weekly_steps=None):
    """设置步数目标"""
    data = load_data(STEP_FILE)
    data["goals"] = {
        "daily_steps": daily_steps,
        "weekly_steps": weekly_steps or daily_steps * 7,
        "active_minutes_daily": 30
    }
    save_data(STEP_FILE, data)
    return data["goals"]


# ========== 数据可视化支持 ==========
def get_health_summary(days=7):
    """获取健康数据汇总（用于可视化）"""
    return {
        "weight": get_health_metrics("weight", days),
        "blood_pressure": get_health_metrics("blood_pressure", days),
        "sleep": get_sleep_stats(days),
        "steps": get_step_stats(days),
        "exercise": load_data(EXERCISE_FILE),
        "diet": load_data(DIET_FILE)
    }


# 初始化数据文件
init_data_files()

if __name__ == "__main__":
    print("健康数据管理模块已加载")
    print(f"数据存储位置: {DATA_DIR}")
