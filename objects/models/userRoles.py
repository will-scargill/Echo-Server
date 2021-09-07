from sqlalchemy import MetaData, Table, Column, String

meta = MetaData()

userRoles = Table(
			"userRoles", meta,
			Column("eID", String),
			Column("roles", String)
		)