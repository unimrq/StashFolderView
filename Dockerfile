FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# 启动 Flask 应用
CMD ["python", "app.py"]

# 设置 Flask 应用的环境变量
ENV base_url=none
ENV username=none
ENV password=none
ENV api_key=none

