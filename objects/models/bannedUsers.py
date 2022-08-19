from sqlalchemy import MetaData, Table, Column, String

meta = MetaData()

bannedUsers = Table(
    "bannedUsers", meta,
    Column("eID", String(64)),
    Column("IP", String(15)),
    Column("dateBanned", String(20)),
    Column("reason", String(100))
)
