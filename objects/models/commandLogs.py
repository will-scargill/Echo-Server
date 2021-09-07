from sqlalchemy import MetaData, Table, Column, String

meta = MetaData()

commandLogs = Table(
			"commandLogs", meta,
			Column("eIDSender", String),
			Column("senderIP", String),
			Column("senderUsername", String),
			Column("eIDTarget", String),
			Column("targetIP", String),
			Column("targetUsername", String),
			Column("channel", String),
			Column("date", String),
			Column("command", String),
			Column("successful", String)
		)