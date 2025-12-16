FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install -e .  # يبني package المحلي
EXPOSE 5000
CMD ["python", "-c", "print('✅ Build successful')"]
