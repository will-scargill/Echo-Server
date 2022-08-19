from sqlalchemy import MetaData, Table, Column, String

meta = MetaData()

userRoles = Table(
    "userRoles", meta,
    Column("eID", String(64)),
    Column("roles", String(256))
)
