#!/bin/bash
# 部署脚本 - NanoBot 健康助理

set -e

echo "🚀 NanoBot 健康助理部署脚本"
echo "================================"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Python 版本
echo -e "${YELLOW}检查 Python 版本...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python 版本: $python_version"

# 检查是否安装了 NanoBot
echo -e "${YELLOW}检查 NanoBot...${NC}"
if ! command -v nanobot &> /dev/null; then
    echo -e "${RED}错误: 未找到 nanobot 命令${NC}"
    echo "请先安装 NanoBot:"
    echo "  pip install -e ../nanobot-whatsapp"
    exit 1
fi
echo -e "${GREEN}✅ NanoBot 已安装${NC}"

# 安装依赖
echo -e "${YELLOW}安装依赖...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✅ 依赖安装完成${NC}"

# 运行测试
echo -e "${YELLOW}运行测试...${NC}"
python3 test_health_assistant.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 测试失败，请检查错误信息${NC}"
    exit 1
fi

# 初始化配置
echo -e "${YELLOW}初始化配置...${NC}"
if [ ! -f ~/.nanobot/config.json ]; then
    echo "首次运行，创建配置..."
    mkdir -p ~/.nanobot
    cp config/nanobot.config.json ~/.nanobot/config.json
    echo -e "${GREEN}✅ 配置已创建: ~/.nanobot/config.json${NC}"
    echo -e "${YELLOW}⚠️ 请编辑配置文件，添加你的 API Key${NC}"
else
    echo -e "${GREEN}✅ 配置已存在${NC}"
fi

# 创建数据目录
echo -e "${YELLOW}创建数据目录...${NC}"
mkdir -p ~/.nanobot/data
echo -e "${GREEN}✅ 数据目录: ~/.nanobot/data${NC}"

# 创建报告目录
echo -e "${YELLOW}创建报告目录...${NC}"
mkdir -p reports
echo -e "${GREEN}✅ 报告目录: reports/${NC}"

echo ""
echo "================================"
echo -e "${GREEN}🎉 部署完成！${NC}"
echo ""
echo "下一步操作:"
echo "1. 编辑配置: nano ~/.nanobot/config.json"
echo "2. 添加 API Key"
echo "3. 连接 WhatsApp: nanobot channels login"
echo "4. 启动服务: nanobot gateway"
echo ""
echo "更多帮助请查看 README.md"
