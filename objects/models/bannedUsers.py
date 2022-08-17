from sqlalchemy import MetaData, Table, Column, String

meta = MetaData()

bannedUsers = Table(
    "bannedUsers", meta,
    Column("eID", String),
    Column("IP", String),
    Column("dateBanned", String),
    Column("reason", String)
)
