from sqlalchemy import MetaData, Table, Column, String

meta = MetaData()

userRoles = Table(
    "userRoles", meta,
    Column("publicKey", String(300)),
    Column("roles", String(256))
)
