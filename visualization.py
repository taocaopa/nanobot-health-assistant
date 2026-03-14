#!/usr/bin/env python3
"""
健康数据可视化模块
生成图表和健康报告
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

try:
    import matplotlib
    matplotlib.use('Agg')  # 无头模式
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    from health_data_manager import (
        load_data, HEALTH_FILE, DIET_FILE, EXERCISE_FILE,
        SLEEP_FILE, STEP_FILE, get_health_summary
    )
except ImportError:
    from .health_data_manager import (
        load_data, HEALTH_FILE, DIET_FILE, EXERCISE_FILE,
        SLEEP_FILE, STEP_FILE, get_health_summary
    )


OUTPUT_DIR = Path(__file__).parent / "reports"
OUTPUT_DIR.mkdir(exist_ok=True)


class HealthVisualizer:
    """健康数据可视化器"""
    
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_weight_chart(self, days=30, output_file=None) -> str:
        """生成体重趋势图"""
        if not MATPLOTLIB_AVAILABLE:
            return self._generate_html_chart("weight", days)
        
        data = load_data(HEALTH_FILE)
        weights = data.get("weight", [])
        
        if not weights:
            return None
        
        # 筛选日期
        cutoff = datetime.now() - timedelta(days=days)
        recent = [w for w in weights 
                  if datetime.strptime(w["date"], "%Y-%m-%d") >= cutoff]
        
        if len(recent) < 2:
            return None
        
        dates = [datetime.strptime(w["date"], "%Y-%m-%d") for w in recent]
        values = [w["value"] for w in recent]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, values, marker='o', linewidth=2, markersize=6, color='#4CAF50')
        ax.fill_between(dates, values, alpha=0.3, color='#4CAF50')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Weight (kg)', fontsize=12)
        ax.set_title('Weight Trend', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        output_path = output_file or self.output_dir / f"weight_chart_{datetime.now().strftime('%Y%m%d')}.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def generate_sleep_chart(self, days=14, output_file=None) -> str:
        """生成睡眠质量图表"""
        if not MATPLOTLIB_AVAILABLE:
            return self._generate_html_chart("sleep", days)
        
        data = load_data(SLEEP_FILE)
        logs = data.get("sleep_logs", [])
        
        if not logs:
            return None
        
        cutoff = datetime.now() - timedelta(days=days)
        recent = [log for log in logs 
                  if datetime.strptime(log["date"], "%Y-%m-%d") >= cutoff]
        
        if len(recent) < 2:
            return None
        
        dates = [datetime.strptime(log["date"], "%Y-%m-%d") for log in recent]
        durations = [log["duration"] for log in recent]
        quality_scores = [log["quality_score"] for log in recent]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # 睡眠时长
        ax1.bar(dates, durations, color='#2196F3', alpha=0.7)
        ax1.axhline(y=8, color='green', linestyle='--', label='Target (8h)')
        ax1.set_ylabel('Duration (hours)', fontsize=12)
        ax1.set_title('Sleep Duration & Quality', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 睡眠质量
        colors = ['#ff5252' if q < 5 else '#ffd740' if q < 7 else '#69f0ae' for q in quality_scores]
        ax2.bar(dates, quality_scores, color=colors, alpha=0.8)
        ax2.set_ylabel('Quality Score (1-10)', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylim(0, 10)
        ax2.grid(True, alpha=0.3)
        
        for ax in [ax1, ax2]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        output_path = output_file or self.output_dir / f"sleep_chart_{datetime.now().strftime('%Y%m%d')}.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def generate_steps_chart(self, days=14, output_file=None) -> str:
        """生成步数图表"""
        if not MATPLOTLIB_AVAILABLE:
            return self._generate_html_chart("steps", days)
        
        data = load_data(STEP_FILE)
        logs = data.get("daily_steps", [])
        
        if not logs:
            return None
        
        cutoff = datetime.now() - timedelta(days=days)
        recent = [log for log in logs 
                  if datetime.strptime(log["date"], "%Y-%m-%d") >= cutoff]
        
        if len(recent) < 2:
            return None
        
        dates = [datetime.strptime(log["date"], "%Y-%m-%d") for log in recent]
        steps = [log["steps"] for log in recent]
        goals = [log.get("goal", 10000) for log in recent]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        colors = ['#4CAF50' if s >= g else '#FFC107' for s, g in zip(steps, goals)]
        bars = ax.bar(dates, steps, color=colors, alpha=0.8)
        ax.axhline(y=10000, color='red', linestyle='--', linewidth=2, label='Goal (10k)')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Steps', fontsize=12)
        ax.set_title('Daily Steps', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        output_path = output_file or self.output_dir / f"steps_chart_{datetime.now().strftime('%Y%m%d')}.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def generate_weekly_report(self, output_file=None) -> str:
        """生成周报"""
        summary = get_health_summary(days=7)
        
        report_lines = [
            "=" * 50,
            "         本周健康报告",
            f"         {datetime.now().strftime('%Y年%m月%d日')}",
            "=" * 50,
            "",
            "📊 步数统计",
            "-" * 30,
        ]
        
        # 步数
        step_stats = summary.get("steps", {})
        if step_stats:
            report_lines.extend([
                f"  平均步数: {step_stats.get('avg_steps', 0):,} 步/天",
                f"  总步数: {step_stats.get('total_steps', 0):,} 步",
                f"  达标天数: {step_stats.get('goal_reached_days', 0)}/{step_stats.get('total_days', 0)} 天",
            ])
        else:
            report_lines.append("  暂无步数数据")
        
        report_lines.extend(["", "😴 睡眠统计", "-" * 30])
        
        # 睡眠
        sleep_stats = summary.get("sleep", {})
        if sleep_stats:
            report_lines.extend([
                f"  平均睡眠: {sleep_stats.get('avg_duration', 0):.1f} 小时/天",
                f"  平均质量: {sleep_stats.get('avg_quality', 0):.1f}/10",
                f"  记录天数: {sleep_stats.get('total_logs', 0)} 天",
            ])
        else:
            report_lines.append("  暂无睡眠数据")
        
        report_lines.extend(["", "💪 运动统计", "-" * 30])
        
        # 运动
        exercise_data = summary.get("exercise", {})
        if exercise_data:
            # 计算本周运动
            total_duration = 0
            total_calories = 0
            for date, day_data in exercise_data.items():
                if isinstance(day_data, dict):
                    total_duration += day_data.get("total_duration", 0)
                    total_calories += day_data.get("total_calories", 0)
            
            report_lines.extend([
                f"  总运动时长: {total_duration} 分钟",
                f"  消耗卡路里: {total_calories} kcal",
            ])
        else:
            report_lines.append("  暂无运动数据")
        
        report_lines.extend(["", "🍎 饮食统计", "-" * 30])
        
        # 饮食
        diet_data = summary.get("diet", {})
        if diet_data:
            total_calories = 0
            days_recorded = 0
            for date, day_data in diet_data.items():
                if isinstance(day_data, dict):
                    total_calories += day_data.get("total_calories", 0)
                    if day_data.get("meals"):
                        days_recorded += 1
            
            avg_calories = total_calories / days_recorded if days_recorded > 0 else 0
            report_lines.extend([
                f"  记录天数: {days_recorded} 天",
                f"  平均摄入: {avg_calories:.0f} kcal/天",
            ])
        else:
            report_lines.append("  暂无饮食数据")
        
        report_lines.extend(["", "=" * 50, "💡 健康建议", "=" * 50])
        
        # 生成建议
        suggestions = []
        
        if step_stats:
            avg = step_stats.get('avg_steps', 0)
            if avg < 5000:
                suggestions.append("  • 步数偏少，建议每天增加步行，目标是 8000-10000 步")
            elif avg >= 10000:
                suggestions.append("  • 步数很棒！保持这个活跃水平")
        
        if sleep_stats:
            avg_duration = sleep_stats.get('avg_duration', 0)
            if avg_duration < 7:
                suggestions.append("  • 睡眠时间不足，建议每晚保证 7-9 小时睡眠")
            avg_quality = sleep_stats.get('avg_quality', 0)
            if avg_quality < 6:
                suggestions.append("  • 睡眠质量有待提高，建议改善睡眠环境，睡前避免屏幕")
        
        if not suggestions:
            suggestions.append("  • 继续记录健康数据，我会为你提供更精准的分析")
        
        report_lines.extend(suggestions)
        report_lines.extend(["", "=" * 50])
        
        report_text = "\n".join(report_lines)
        
        # 保存报告
        output_path = output_file or self.output_dir / f"weekly_report_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        return report_text
    
    def generate_html_report(self, days=7, output_file=None) -> str:
        """生成 HTML 格式的健康报告"""
        summary = get_health_summary(days=days)
        
        # 准备数据
        step_stats = summary.get("steps", {})
        sleep_stats = summary.get("sleep", {})
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>健康报告 - {datetime.now().strftime('%Y年%m月%d日')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; font-size: 1.1em; }}
        .content {{ padding: 40px; }}
        .section {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
        }}
        .section h2 {{
            color: #333;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .suggestions {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
        }}
        .suggestions h2 {{ margin-bottom: 15px; }}
        .suggestions ul {{ list-style: none; }}
        .suggestions li {{
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }}
        .suggestions li:last-child {{ border-bottom: none; }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 健康报告</h1>
            <p>{datetime.now().strftime('%Y年%m月%d日')} | 过去{days}天数据统计</p>
        </div>
        
        <div class="content">
            <!-- 步数统计 -->
            <div class="section">
                <h2>👟 步数统计</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{step_stats.get('avg_steps', 0):,}</div>
                        <div class="stat-label">平均步数/天</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{step_stats.get('total_steps', 0):,}</div>
                        <div class="stat-label">总步数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{step_stats.get('goal_reached_days', 0)}/{step_stats.get('total_days', 0)}</div>
                        <div class="stat-label">达标天数</div>
                    </div>
                </div>
            </div>
            
            <!-- 睡眠统计 -->
            <div class="section">
                <h2>😴 睡眠统计</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{sleep_stats.get('avg_duration', 0):.1f}h</div>
                        <div class="stat-label">平均睡眠时长</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{sleep_stats.get('avg_quality', 0):.1f}</div>
                        <div class="stat-label">平均质量评分</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{sleep_stats.get('total_logs', 0)}</div>
                        <div class="stat-label">记录天数</div>
                    </div>
                </div>
            </div>
            
            <!-- 健康建议 -->
            <div class="suggestions">
                <h2>💡 健康建议</h2>
                <ul>
                    <li>继续记录健康数据，建立长期健康档案</li>
                    <li>保持规律作息，每晚争取 7-9 小时睡眠</li>
                    <li>每天至少进行 30 分钟中等强度运动</li>
                    <li>饮食均衡，多吃蔬菜水果，控制糖分摄入</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>由 NanoBot 健康助理生成 | 数据仅供参考，不构成医疗建议</p>
        </div>
    </div>
</body>
</html>"""
        
        output_path = output_file or self.output_dir / f"health_report_{datetime.now().strftime('%Y%m%d')}.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def _generate_html_chart(self, chart_type: str, days: int) -> str:
        """当 matplotlib 不可用时生成简单的 HTML 图表"""
        # 这里可以生成基于 JavaScript 的图表
        return self.generate_html_report(days=days)


def main():
    """测试可视化功能"""
    viz = HealthVisualizer()
    
    print("生成健康报告中...")
    
    # 生成各类图表
    weight_chart = viz.generate_weight_chart()
    if weight_chart:
        print(f"✅ 体重图表: {weight_chart}")
    
    sleep_chart = viz.generate_sleep_chart()
    if sleep_chart:
        print(f"✅ 睡眠图表: {sleep_chart}")
    
    steps_chart = viz.generate_steps_chart()
    if steps_chart:
        print(f"✅ 步数图表: {steps_chart}")
    
    # 生成报告
    report = viz.generate_weekly_report()
    print(f"\n📊 本周健康报告:\n{report}")
    
    html_report = viz.generate_html_report()
    print(f"\n✅ HTML报告: {html_report}")


if __name__ == "__main__":
    main()
