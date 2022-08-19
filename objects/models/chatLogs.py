from sqlalchemy import MetaData, Table, Column, String

meta = MetaData()

chatLogs = Table(
    "chatLogs", meta,
    Column("eID", String(64)),
    Column("IP", String(15)),
    Column("username", String(64)),
    Column("channel", String(64)),
    Column("date", String(64)),
    Column("message", String(256))
)
