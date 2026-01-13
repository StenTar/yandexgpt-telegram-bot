# src/universal_logger.py
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class UniversalLogger:
    """Универсальный логгер, который может писать в PostgreSQL или файл."""
    
    def __init__(self):
        self.log_type = os.getenv("LOG_TYPE", "postgres").lower()
        self.log_file = os.getenv("LOG_FILE", "/opt/ytb/logs/bot.log")
        
        # Создаем папку для логов если ее нет
        if self.log_type == "file":
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Инициализируем нужный логгер
        if self.log_type == "postgres":
            self._init_postgres_logger()
        elif self.log_type == "file":
            self._init_file_logger()
        else:
            print(f"⚠️ Неизвестный LOG_TYPE: {self.log_type}, использую файловый логгер")
            self.log_type = "file"
            self._init_file_logger()
    
    def _init_postgres_logger(self):
        """Инициализировать PostgreSQL логгер."""
        try:
            from .postgres_logger import pg_logger
            self.pg_logger = pg_logger
            print("✅ Используется PostgreSQL логгер")
        except ImportError as e:
            print(f"❌ Не удалось импортировать PostgreSQL логгер: {e}")
            print("⚠️ Переключаюсь на файловый логгер")
            self.log_type = "file"
            self._init_file_logger()
    
    def _init_file_logger(self):
        """Инициализировать файловый логгер."""
        # Создаем логгер
        self.logger = logging.getLogger("telegram_bot")
        self.logger.setLevel(logging.INFO)
        
        # Форматтер
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Файловый хендлер
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        
        # Очищаем старые хендлеры и добавляем новый
        self.logger.handlers.clear()
        self.logger.addHandler(file_handler)
        
        print(f"✅ Используется файловый логгер: {self.log_file}")
    
    def log(self, level: str, username: str, user_id: int, message: str, error: str = None):
        """
        Записать лог в выбранное место.
        
        :param level: INFO, ERROR, WARNING, DEBUG
        :param username: Имя пользователя Telegram
        :param user_id: ID пользователя Telegram
        :param message: Текст сообщения
        :param error: Текст ошибки (если есть)
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {level} - {username} ({user_id}): {message}"
        if error:
            log_message += f" | Ошибка: {error}"
        
        if self.log_type == "postgres" and hasattr(self, 'pg_logger'):
            # Логируем в PostgreSQL
            self.pg_logger.log(level, username, user_id, message, error)
            # Также выводим в консоль для отладки
            print(log_message)
        elif self.log_type == "file":
            # Логируем в файл
            if level == "ERROR":
                self.logger.error(log_message)
            elif level == "WARNING":
                self.logger.warning(log_message)
            else:
                self.logger.info(log_message)
            # Также выводим в консоль
            print(log_message)
    
    def close(self):
        """Закрыть соединения."""
        if self.log_type == "postgres" and hasattr(self, 'pg_logger'):
            self.pg_logger.close()

# Глобальный экземпляр для удобного использования
universal_logger = UniversalLogger()
