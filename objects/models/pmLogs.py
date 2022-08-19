from sqlalchemy import MetaData, Table, Column, String

meta = MetaData()

pmLogs = Table(
    "pmLogs", meta,
    Column("eIDSender", String(64)),
    Column("senderIP", String(15)),
    Column("senderUsername", String(64)),
    Column("eIDTarget", String(64)),
    Column("targetIP", String(15)),
    Column("targetUsername", String(64)),
    Column("channel", String(64)),
    Column("date", String(64)),
    Column("message", String(256))
)
