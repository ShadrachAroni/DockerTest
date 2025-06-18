FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install flask docker requests

EXPOSE 5000
CMD ["python", "load_balancer.py"]
