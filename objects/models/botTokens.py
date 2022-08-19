from sqlalchemy import MetaData, Table, Column, String, Integer

meta = MetaData()

botTokens = Table(
    "botTokens", meta,
    Column("id", Integer, primary_key=True),
    Column("token", String(64))
)
