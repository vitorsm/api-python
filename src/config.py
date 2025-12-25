import os

API_TOKEN_EXPIRATION_HOURS = int(os.getenv("API_TOKEN_EXPIRATION_HOURS", "12"))
API_TOKEN_SECRET = os.getenv("API_TOKEN_SECRET", "aidjfaoijfididid")

DB_USERNAME = os.getenv("DB_USERNAME", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "app_db_name")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_CONNECTION_STR = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

FILE_REPOSITORY = os.getenv("FILE_REPOSITORY", ".files")

# if you will allow cors outside (nginx for example) it should be false to avoid duplicate headers
ADD_ALLOW_CORS = os.getenv("ADD_ALLOW_CORS", "false") == "true"