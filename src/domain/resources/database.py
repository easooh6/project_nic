from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from settings import settings_db

engine = create_engine(
    url=settings_db.DATABASE_URL_psycopg,
    echo=False)
#LocalSession - sessionmaker(autoflush=False, autocommit=False)
with engine.connect() as conn:
    res = conn.execute(text("SELECT VERSION()"))
    print(f"{res.first()}")    