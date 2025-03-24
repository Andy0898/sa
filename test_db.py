from sqlalchemy import text
from models.base import engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_db_connection():
    try:
        # 测试数据库连接
        with engine.connect() as connection:
            result = connection.execute(text("SELECT VERSION()"))
            version = result.scalar()
            logger.info(f"Successfully connected to MySQL. Version: {version}")
            
            # 获取所有表名
            result = connection.execute(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'sadb'"
            ))
            tables = [row[0] for row in result]
            logger.info("Available tables in sadb database:")
            for table in tables:
                logger.info(f"- {table}")
                
            return True
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return False

if __name__ == "__main__":
    test_db_connection() 