FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["python","-c","from event_platform import EventBus; print('event bus ready')"]
