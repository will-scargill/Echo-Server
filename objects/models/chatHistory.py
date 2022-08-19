from sqlalchemy import MetaData, Table, Column, String, Integer

meta = MetaData()

chatHistory = Table(
    "chatHistory", meta,
    Column("username", String(64)),
    Column("channel", String(64)),
    Column("date", String(64)),
    Column("message", String(256)),
    Column("colour", String(64)),
    Column("realtime", Integer),
)
