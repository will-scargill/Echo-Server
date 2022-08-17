from sqlalchemy import MetaData, Table, Column, String

meta = MetaData()

chatLogs = Table(
    "chatLogs", meta,
    Column("eID", String),
    Column("IP", String),
    Column("username", String),
    Column("channel", String),
    Column("date", String),
    Column("message", String)
)
