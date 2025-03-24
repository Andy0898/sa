from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from core.config import settings
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建数据库引擎，配置连接池
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,  # 连接池大小
    max_overflow=10,  # 超过pool_size后最多可以创建的连接数
    pool_timeout=30,  # 连接池中没有可用连接的等待时间
    pool_recycle=1800,  # 连接在连接池中重复使用的时间间隔（秒）
    echo=False  # 设置为True可以输出SQL语句，用于调试
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()

def get_db():
    """获取数据库会话的依赖函数"""
    db = SessionLocal()
    try:
        yield db
        logger.debug("Database session created successfully")
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        db.close()
        logger.debug("Database session closed") 