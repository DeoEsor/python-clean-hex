from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "stock_service"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_CONSUMER_GROUP: str = "stock_service"
    KAFKA_TRANSACTIONS_TOPIC: str = "transactions"
    
    # Temporal settings
    TEMPORAL_HOST: str = "localhost:7233"
    TEMPORAL_TASK_QUEUE: str = "transactions"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings() 