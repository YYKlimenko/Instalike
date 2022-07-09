from auth.models import User


DATABASE_FILE = 'core/database.db'
DATABASE_URL = 'postgresql+psycopg2://postgres:POSTGRES@localhost:5432/postgres'
MEDIA_URL = 'media/'
SECRET_KEY = 'ABCD'
USER_MODEL = User
USER_FIELD = 'user_id'
