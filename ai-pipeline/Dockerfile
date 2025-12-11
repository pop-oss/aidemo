# AI 代码流水线 Docker 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY orchestrator/ ./orchestrator/
COPY example_app/ ./example_app/

# 创建输出目录
RUN mkdir -p /app/output

# 设置卷
VOLUME ["/app/output"]

# 健康检查 (仅适用于微服务模式)
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# 默认命令:显示帮助信息
CMD ["python", "orchestrator/orchestrator.py", "--help"]

# 使用示例:
# docker run --rm \
#   -e OPENAI_API_KEY=your_key \
#   -v $(pwd)/output:/app/output \
#   ai-pipeline \
#   python orchestrator/orchestrator.py --requirement "创建一个 REST API"
