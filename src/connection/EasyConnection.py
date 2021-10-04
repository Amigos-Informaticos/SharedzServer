import mysql.connector
from mysql.connector import Error

from src.configuration.ConfigServer import ConfigServer


class EasyConnection:
	static_host = ""
	static_database = ""
	static_user = ""
	static_password = ""

	def __init__(self, host=None, database=None, user=None, password=None):
		if host is not None:
			self.user = user
			self.password = password
			self.database = database
			self.host = host
		elif EasyConnection.static_host != "":
			self.host = EasyConnection.static_host
			self.database = EasyConnection.static_database
			self.user = EasyConnection.static_user
			self.password = EasyConnection.static_password

	@staticmethod
	def build_from_static():
		connection = None
		if EasyConnection.static_host == "":
			config_server = ConfigServer("petMe")
			results = config_server.patch(["db_name", "db_host", "db_user", "db_password"]).json()

			EasyConnection.static_host = results["db_host"]
			EasyConnection.static_database = results["db_name"]
			EasyConnection.static_user = results["db_user"]
			EasyConnection.static_password = results["db_password"]

			connection = EasyConnection()
			connection.host = results["db_host"]
			connection.database = results["db_name"]
			connection.user = results["db_user"]
			connection.password = results["db_password"]
		elif EasyConnection.static_host != "":
			connection = EasyConnection()
			connection.host = EasyConnection.static_host
			connection.database = EasyConnection.static_database
			connection.user = EasyConnection.static_user
			connection.password = EasyConnection.static_password
		return connection

	def connect(self, include_params: bool = False):
		self.connection = mysql.connector.connect(
			host=self.host,
			database=self.database,
			user=self.user,
			password=self.password
		)
		return self.connection.cursor(prepared=include_params)

	def close_connection(self):
		if self.connection.is_connected():
			self.connection.close()

	def send_query(self, query, values: list = None):
		executed = False
		if self.host is not None:
			parameters: tuple = ()
			try:
				if values is not None:
					cursor = self.connect(True)
					parameters = tuple(values)
				else:
					cursor = self.connect()
				cursor.execute(query, parameters)
				self.connection.commit()
				executed = True
			except Error as error:
				print(f"Problem connecting to the database: {error}")
			finally:
				self.close_connection()
		return executed

	def select(self, query, values: list = None):
		results = []
		if self.host is not None:
			parameters: tuple = ()
			try:
				if values is not None:
					cursor = self.connect(True)
					parameters = tuple(values)
				else:
					cursor = self.connect(False)
				cursor.execute(query, parameters)
				tmp_results = cursor.fetchall()
				for row in tmp_results:
					results.append(dict(zip(cursor.column_names, row)))
			except Error as error:
				print(f"Problem connecting to the database: {error}")
			finally:
				self.close_connection()
		return results
