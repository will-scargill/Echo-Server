from sqlalchemy import MetaData, Table, Column, String, Integer

meta = MetaData()

chatHistory = Table(
			"chatHistory", meta,
			Column("username", String),
			Column("channel", String),
			Column("date", String),
			Column("message", String),
			Column("colour", String),
			Column("realtime", Integer),
		)