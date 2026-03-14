# 部署指南 - NanoBot 健康助理

## 1. 部署架构

### 1.1 单机部署

```
┌─────────────────────────────────────────────┐
│              单机部署架构                    │
├─────────────────────────────────────────────┤
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │            用户设备                    │ │
│  │       (手机/电脑)                     │ │
│  └───────────────┬───────────────────────┘ │
│                  │ WhatsApp               │
│                  ▼                        │
│  ┌───────────────────────────────────────┐ │
│  │           服务器/PC                    │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │   NanoBot Gateway (Port 5000)   │ │ │
│  │  │   - WebSocket Handler           │ │ │
│  │  │   - Message Router              │ │ │
│  │  └─────────────────────────────────┘ │ │
│  │                  │                    │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │   Health Assistant Core         │ │ │
│  │  │   - Intent Recognition          │ │ │
│  │  │   - Skill Router                │ │ │
│  │  │   - Response Generator          │ │ │
│  │  └─────────────────────────────────┘ │ │
│  │                  │                    │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │   Local Data Storage            │ │ │
│  │  │   ~/.nanobot/data/              │ │ │
│  │  │   - JSON Files                  │ │ │
│  │  │   - Reports                     │ │ │
│  │  └─────────────────────────────────┘ │ │
│  └───────────────────────────────────────┘ │
│                                             │
└─────────────────────────────────────────────┘
```

### 1.2 系统要求

| 组件 | 最低要求 | 推荐配置 |
|------|---------|---------|
| CPU | 2 核 | 4 核 |
| RAM | 2 GB | 4 GB |
| 磁盘 | 10 GB | 50 GB |
| 网络 | 10 Mbps | 100 Mbps |
| 系统 | Ubuntu 20.04 | Ubuntu 22.04 |

---

## 2. 安装部署

### 2.1 快速部署

```bash
# 一键部署脚本
chmod +x deploy.sh
./deploy.sh
```

### 2.2 手动部署

#### Step 1: 环境准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装依赖
sudo apt install -y python3 python3-pip python3-venv git curl

# 验证安装
python3 --version  # Python 3.8+
git --version      # Git 2.25+
```

#### Step 2: 下载项目

```bash
# 克隆仓库
git clone https://github.com/taocaopa/nanobot-health-assistant.git
cd nanobot-health-assistant

# 或下载最新 Release
curl -L -o nanobot-health-assistant.tar.gz \
    https://github.com/taocaopa/nanobot-health-assistant/archive/refs/tags/v1.0.0.tar.gz
tar -xzf nanobot-health-assistant.tar.gz
cd nanobot-health-assistant-1.0.0
```

#### Step 3: 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装 Python 依赖
pip install --upgrade pip
pip install -r requirements.txt

# 验证安装
pip list | grep -E "matplotlib|numpy|pandas"
```

#### Step 4: 安装 NanoBot

```bash
# 安装 NanoBot 框架
pip install nanobot

# 验证安装
nanobot --version
# 输出: nanobot 1.0.0
```

#### Step 5: 配置

```bash
# 初始化配置
nanobot onboard

# 编辑配置文件
nano ~/.nanobot/config.json
```

配置示例:
```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-your-api-key"
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-3.5-sonnet",
      "provider": "openrouter",
      "systemPrompt": "你是用户的个人健康助理...",
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
  }
}
```

#### Step 6: 连接 WhatsApp

```bash
# 连接 WhatsApp
nanobot channels login

# 扫描终端显示的二维码
# 等待 "Connected" 提示
```

#### Step 7: 启动服务

```bash
# 方式 1: 前台运行（调试）
nanobot gateway

# 方式 2: 后台运行
nohup nanobot gateway > health_assistant.log 2>&1 &

# 方式 3: Systemd 服务（推荐用于生产）
sudo nano /etc/systemd/system/health-assistant.service
```

Systemd 服务配置:
```ini
[Unit]
Description=NanoBot Health Assistant
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/nanobot-health-assistant
ExecStart=/home/your-username/nanobot-health-assistant/venv/bin/nanobot gateway
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用服务:
```bash
sudo systemctl daemon-reload
sudo systemctl enable health-assistant
sudo systemctl start health-assistant

# 查看状态
sudo systemctl status health-assistant

# 查看日志
sudo journalctl -u health-assistant -f
```

---

## 3. Docker 部署

### 3.1 Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装 NanoBot
RUN pip install nanobot

# 复制项目代码
COPY . .

# 创建数据目录
RUN mkdir -p /root/.nanobot/data

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["nanobot", "gateway"]
```

### 3.2 Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  health-assistant:
    build: .
    container_name: nanobot-health
    ports:
      - "5000:5000"
    volumes:
      - ./data:/root/.nanobot/data
      - ./config:/root/.nanobot/config
      - ./reports:/app/reports
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    restart: unless-stopped
    
  # 可选: 监控
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

### 3.3 部署命令

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 4. 生产环境优化

### 4.1 性能优化

```python
# config/production.py

# 缓存配置
CACHE_CONFIG = {
    'enabled': True,
    'ttl': 300,  # 5分钟
    'max_size': 1000
}

# 并发配置
CONCURRENCY_CONFIG = {
    'max_workers': 4,
    'max_connections': 100
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'handlers': ['file', 'console']
}
```

### 4.2 监控配置

```python
# monitoring/health_check.py

import psutil
from datetime import datetime

class SystemMonitor:
    """系统监控器"""
    
    def get_metrics(self):
        """获取系统指标"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'timestamp': datetime.now().isoformat()
        }
    
    def check_health(self):
        """健康检查"""
        metrics = self.get_metrics()
        
        alerts = []
        if metrics['cpu_percent'] > 80:
            alerts.append('CPU usage high')
        if metrics['memory_percent'] > 80:
            alerts.append('Memory usage high')
        if metrics['disk_usage'] > 90:
            alerts.append('Disk usage critical')
        
        return {
            'status': 'unhealthy' if alerts else 'healthy',
            'metrics': metrics,
            'alerts': alerts
        }
```

### 4.3 备份策略

```bash
#!/bin/bash
# backup.sh - 数据备份脚本

BACKUP_DIR="/backup/health-assistant"
DATA_DIR="$HOME/.nanobot/data"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份数据
tar -czf "$BACKUP_DIR/data_$DATE.tar.gz" -C "$DATA_DIR" .

# 保留最近 30 天的备份
find "$BACKUP_DIR" -name "data_*.tar.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_DIR/data_$DATE.tar.gz"
```

定时备份:
```bash
# 添加到 crontab
crontab -e

# 每天凌晨 2 点备份
0 2 * * * /path/to/backup.sh >> /var/log/health-assistant-backup.log 2>&1
```

---

## 5. 升级维护

### 5.1 版本升级

```bash
# 1. 备份数据
./backup.sh

# 2. 拉取最新代码
git pull origin main

# 3. 更新依赖
pip install -r requirements.txt --upgrade

# 4. 重启服务
sudo systemctl restart health-assistant

# 5. 验证升级
curl http://localhost:5000/health
```

### 5.2 回滚策略

```bash
# 1. 停止服务
sudo systemctl stop health-assistant

# 2. 恢复代码
git checkout v1.0.0

# 3. 恢复数据
tar -xzf /backup/health-assistant/data_20260315_020000.tar.gz -C ~/.nanobot/data/

# 4. 重启服务
sudo systemctl start health-assistant
```

---

## 6. 故障排查

### 6.1 常见问题

#### 问题 1: 无法连接到 WhatsApp

```bash
# 检查日志
tail -f health_assistant.log

# 常见原因:
# 1. 网络问题
ping web.whatsapp.com

# 2. 二维码过期
# 重新连接
nanobot channels login

# 3. 多设备冲突
# 在手机上退出其他 WhatsApp Web 会话
```

#### 问题 2: 数据丢失

```bash
# 检查数据目录
ls -la ~/.nanobot/data/

# 从备份恢复
tar -xzf /backup/health-assistant/data_latest.tar.gz -C ~/.nanobot/data/
```

#### 问题 3: API 限流

```python
# 添加重试机制
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def call_api():
    # API 调用
    pass
```

### 6.2 日志分析

```bash
# 查看错误日志
grep ERROR health_assistant.log

# 统计请求量
grep "Request" health_assistant.log | wc -l

# 分析响应时间
grep "Response time" health_assistant.log | awk '{print $4}'
```

---

## 7. 安全加固

### 7.1 文件权限

```bash
# 设置数据目录权限
chmod 700 ~/.nanobot/
chmod 600 ~/.nanobot/config.json
chmod 600 ~/.nanobot/data/*.json

# 设置日志权限
chmod 644 health_assistant.log
```

### 7.2 防火墙配置

```bash
# 只允许本地访问 (如果不需要远程管理)
sudo ufw allow from 127.0.0.1 to any port 5000

# 或配置 Nginx 反向代理
sudo nano /etc/nginx/sites-available/health-assistant
```

Nginx 配置:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 8. 自动化部署 (CI/CD)

### 8.1 GitHub Actions 部署

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        script: |
          cd ~/nanobot-health-assistant
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          sudo systemctl restart health-assistant
```

### 8.2 环境变量

```bash
# .env 文件 (不要提交到 Git)
OPENROUTER_API_KEY=sk-or-v1-xxxx
GITHUB_TOKEN=ghp_xxxx
SERVER_HOST=your-server.com
SERVER_USER=ubuntu
```

---

## 9. 扩展部署

### 9.1 多实例部署

```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  health-assistant-1:
    build: .
    ports:
      - "5001:5000"
    volumes:
      - ./data1:/root/.nanobot/data
  
  health-assistant-2:
    build: .
    ports:
      - "5002:5000"
    volumes:
      - ./data2:/root/.nanobot/data
  
  nginx:
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### 9.2 云端部署

#### AWS EC2

```bash
# 1. 创建 EC2 实例 (t3.medium)
# 2. 配置安全组 (开放 5000 端口)
# 3. SSH 连接到实例
ssh -i key.pem ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com

# 4. 按手动部署步骤安装
# ...
```

#### Google Cloud Run

```bash
# 1. 构建容器
gcloud builds submit --tag gcr.io/PROJECT_ID/health-assistant

# 2. 部署到 Cloud Run
gcloud run deploy health-assistant \
  --image gcr.io/PROJECT_ID/health-assistant \
  --platform managed \
  --allow-unauthenticated
```

---

## 10. 部署清单

### 部署前检查

- [ ] 服务器满足最低配置要求
- [ ] 已安装 Python 3.8+
- [ ] 已配置 API Key
- [ ] 已备份现有数据（如有）

### 部署中检查

- [ ] 依赖安装成功
- [ ] 配置文件正确
- [ ] WhatsApp 连接成功
- [ ] 服务启动无错误

### 部署后检查

- [ ] 响应测试通过
- [ ] 数据记录正常
- [ ] 可视化功能正常
- [ ] 监控告警配置完成
- [ ] 备份策略生效

---

*文档版本: 1.0.0*  
*作者: Chief AI Architect*  
*日期: 2026-03-15*
