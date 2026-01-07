# src/postgres_logger.py
import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

class PostgresLogger:
    """Логгер, записывающий сообщения в таблицу PostgreSQL."""
    
    def __init__(self):
        self.host = os.getenv("DB_HOST", "192.168.1.249")
        self.port = os.getenv("DB_PORT", "5432")
        self.database = os.getenv("DB_NAME", "ytb")
        self.user = os.getenv("DB_USER", "ytb_admin")
        self.password = os.getenv("DB_PASSWORD")
        
        if not self.password:
            raise ValueError("❌ DB_PASSWORD не указан в .env")
        
        self.conn = None
        self._connect()
    
    def _connect(self):
        """Установить подключение к PostgreSQL."""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor
            )
            print(f"✅ Подключение к PostgreSQL ({self.host}:{self.port}) установлено")
        except Exception as e:
            print(f"❌ Ошибка подключения к PostgreSQL: {e}")
            self.conn = None
    
    def log(self, level: str, username: str, user_id: int, message: str, error: str = None):
        """
        Записать лог в базу данных.
        
        :param level: Уровень лога (INFO, ERROR, WARNING, DEBUG)
        :param username: Имя пользователя Telegram
        :param user_id: ID пользователя Telegram
        :param message: Текст сообщения/лога
        :param error: Текст ошибки (если есть)
        """
        if not self.conn:
            print("⚠️ Нет подключения к БД, лог не записан")
            return
        
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO bot_logs (level, username, user_id, message, error)
                    VALUES (%s, %s, %s, %s, %s)
                """, (level, username, user_id, message, error))
                self.conn.commit()
                
        except Exception as e:
            print(f"❌ Ошибка записи лога в БД: {e}")
            # Попробуем переподключиться при следующем вызове
            self.conn = None
    
    def close(self):
        """Закрыть соединение с БД."""
        if self.conn:
            self.conn.close()
            print("✅ Соединение с PostgreSQL закрыто")

# Глобальный экземпляр логгера для удобного использования
pg_logger = PostgresLogger()
