import databases
import sqlalchemy
import aiosqlite
import uvicorn
from fastapi import FastAPI

DATABASE_URL = "sqlite:///my_database.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table("users", metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("name", sqlalchemy.String(32)),
                         sqlalchemy.Column("surname", sqlalchemy.String(32)),
                         sqlalchemy.Column("email", sqlalchemy.String(128)),
                         sqlalchemy.Column("password", sqlalchemy.String(32)),
                         )

products = sqlalchemy.Table("products", metadata,
                            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column("title", sqlalchemy.String(50)),
                            sqlalchemy.Column("description", sqlalchemy.String(300)),
                            sqlalchemy.Column("price", sqlalchemy.Integer)
                            )

orders = sqlalchemy.Table("orders", metadata,
                          sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
                          sqlalchemy.Column("prod_id", sqlalchemy.ForeignKey("products.id")),
                          sqlalchemy.Column("date", sqlalchemy.String),
                          sqlalchemy.Column("status", sqlalchemy.String(20))
                          )

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  
)
metadata.create_all(engine)