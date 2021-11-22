from src.core.config import settings

loglevel = settings.LOG_LEVEL
bind = f"{settings.HOST}:{settings.PORT}"
workers = settings.WORKERS
worker_connections = 1000
max_requests = int(workers * worker_connections)
max_requests_jitter = 5
keepalive = 120
timeout = 120
worker_class = "uvicorn.workers.UvicornWorker"
forwarded_allow_ips = "*"
