import os
from loguru import logger

# 配置日志文件夹路径
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

# 配置日志记录器
logger.add(
    sink=os.path.join(log_dir, "{time:YYYY-MM-DD}.log"),  # 日志文件路径，按天生成日志文件
    level="INFO",  # 只记录 INFO 及以上级别的日志
    rotation="1 week",  # 日志轮转周期为一周
    compression="zip",  # 日志文件压缩格式为 zip
    enqueue=True,  # 异步写入日志，避免阻塞主线程
    encoding="utf-8",  # 日志文件编码为 UTF-8
    retention="30 days",  # 日志文件保留 30 天
    serialize=False,  # 不序列化日志记录，使用普通文本格式
    backtrace=True,  # 记录异常的回溯信息
    diagnose=True,  # 记录诊断信息，如文件名和行号
    catch=True,  # 捕获并记录所有异常
)

log = logger
