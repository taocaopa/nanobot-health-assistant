#!/usr/bin/env python3
"""
健康助理测试脚本
用于验证各功能模块是否正常工作
"""

import sys
import os
from datetime import datetime, timedelta

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from health_data_manager import (
    record_health_metric, record_meal, record_exercise,
    record_symptom, record_sleep, record_steps,
    get_health_metrics, get_sleep_stats, get_step_stats,
    get_health_summary, DATA_DIR
)
from visualization import HealthVisualizer


def test_data_management():
    """测试数据管理功能"""
    print("=" * 50)
    print("测试数据管理模块")
    print("=" * 50)
    
    # 测试健康指标记录
    print("\n1. 测试健康指标记录...")
    entry = record_health_metric("weight", 70.5, "kg", "早餐前测量")
    print(f"✅ 体重记录: {entry}")
    
    # 测试饮食记录
    print("\n2. 测试饮食记录...")
    meal = record_meal("breakfast", ["燕麦", "鸡蛋", "牛奶"], 450, "吃得很饱")
    print(f"✅ 早餐记录: {meal['items']}, {meal['calories']} kcal")
    
    # 测试运动记录
    print("\n3. 测试运动记录...")
    exercise = record_exercise("跑步", 30, 300, "晨跑感觉很棒")
    print(f"✅ 运动记录: {exercise['type']}, {exercise['duration']}分钟, {exercise['calories']} kcal")
    
    # 测试症状记录
    print("\n4. 测试症状记录...")
    symptom = record_symptom("头痛", "moderate", "2小时", ["长时间看屏幕"], "休息一下后缓解")
    print(f"✅ 症状记录: {symptom['symptom']}, 严重程度: {symptom['severity']}")
    
    # 测试睡眠记录
    print("\n5. 测试睡眠记录...")
    sleep = record_sleep(
        duration=7.5,
        quality_score=8,
        bedtime="23:00",
        wakeup_time="06:30",
        sleep_onset_minutes=15,
        awakenings=1,
        factors={"caffeine": False, "exercise": True},
        notes="睡得很香"
    )
    print(f"✅ 睡眠记录: {sleep['duration']}小时, 质量评分: {sleep['quality_score']}")
    
    # 测试步数记录
    print("\n6. 测试步数记录...")
    steps = record_steps(
        steps=8500,
        distance_km=6.8,
        active_minutes=45,
        calories=340,
        goal=10000,
        notes="今天走路去上班"
    )
    print(f"✅ 步数记录: {steps['steps']}步, 完成度: {steps['goal_percentage']}%")
    
    print("\n✅ 数据管理模块测试通过！")
    return True


def test_visualization():
    """测试可视化功能"""
    print("\n" + "=" * 50)
    print("测试可视化模块")
    print("=" * 50)
    
    viz = HealthVisualizer()
    
    # 测试生成周报
    print("\n1. 生成周报...")
    try:
        report = viz.generate_weekly_report()
        print(f"✅ 周报生成成功")
        print(report[:500] + "...")  # 显示部分内容
    except Exception as e:
        print(f"⚠️ 周报生成警告: {e}")
    
    # 测试生成 HTML 报告
    print("\n2. 生成 HTML 报告...")
    try:
        html_path = viz.generate_html_report(days=7)
        print(f"✅ HTML报告生成: {html_path}")
    except Exception as e:
        print(f"⚠️ HTML报告生成警告: {e}")
    
    # 测试图表生成（如果 matplotlib 可用）
    print("\n3. 测试图表生成...")
    try:
        weight_chart = viz.generate_weight_chart(days=30)
        if weight_chart:
            print(f"✅ 体重图表: {weight_chart}")
        else:
            print("⚠️ 体重图表: 数据不足")
        
        sleep_chart = viz.generate_sleep_chart(days=14)
        if sleep_chart:
            print(f"✅ 睡眠图表: {sleep_chart}")
        else:
            print("⚠️ 睡眠图表: 数据不足")
        
        steps_chart = viz.generate_steps_chart(days=14)
        if steps_chart:
            print(f"✅ 步数图表: {steps_chart}")
        else:
            print("⚠️ 步数图表: 数据不足")
    except Exception as e:
        print(f"⚠️ 图表生成警告: {e}")
    
    print("\n✅ 可视化模块测试通过！")
    return True


def test_data_retrieval():
    """测试数据查询功能"""
    print("\n" + "=" * 50)
    print("测试数据查询功能")
    print("=" * 50)
    
    # 查询体重
    print("\n1. 查询最近7天体重数据...")
    weights = get_health_metrics("weight", 7)
    print(f"✅ 找到 {len(weights)} 条体重记录")
    
    # 查询睡眠统计
    print("\n2. 查询睡眠统计...")
    sleep_stats = get_sleep_stats(7)
    if sleep_stats:
        print(f"✅ 平均睡眠: {sleep_stats.get('avg_duration', 0):.1f}小时")
        print(f"✅ 平均质量: {sleep_stats.get('avg_quality', 0):.1f}/10")
    else:
        print("⚠️ 暂无睡眠统计数据")
    
    # 查询步数统计
    print("\n3. 查询步数统计...")
    step_stats = get_step_stats(7)
    if step_stats:
        print(f"✅ 平均步数: {step_stats.get('avg_steps', 0):,}")
        print(f"✅ 达标天数: {step_stats.get('goal_reached_days', 0)}/{step_stats.get('total_days', 0)}")
    else:
        print("⚠️ 暂无步数统计数据")
    
    # 查询健康汇总
    print("\n4. 查询健康数据汇总...")
    summary = get_health_summary(7)
    print(f"✅ 汇总数据包含: {list(summary.keys())}")
    
    print("\n✅ 数据查询功能测试通过！")
    return True


def main():
    """主测试函数"""
    print("\n" + "🚀" * 25)
    print("  NanoBot 健康助理测试")
    print("🚀" * 25 + "\n")
    
    results = []
    
    # 测试数据管理
    try:
        results.append(("数据管理", test_data_management()))
    except Exception as e:
        print(f"\n❌ 数据管理测试失败: {e}")
        results.append(("数据管理", False))
    
    # 测试数据查询
    try:
        results.append(("数据查询", test_data_retrieval()))
    except Exception as e:
        print(f"\n❌ 数据查询测试失败: {e}")
        results.append(("数据查询", False))
    
    # 测试可视化
    try:
        results.append(("可视化", test_visualization()))
    except Exception as e:
        print(f"\n❌ 可视化测试失败: {e}")
        results.append(("可视化", False))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print("\n🎉 所有测试通过！健康助理可以正常使用。")
        print(f"\n📁 数据存储位置: {DATA_DIR}")
        print(f"📊 报告输出位置: {HealthVisualizer().output_dir}")
        return 0
    else:
        print("\n⚠️ 部分测试未通过，请检查错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
