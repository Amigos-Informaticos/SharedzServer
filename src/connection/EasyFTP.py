from ftplib import FTP, error_perm

from src.configuration.ConfigServer import ConfigServer


class EasyFTP:
	static_host = ""
	static_user = ""
	static_password = ""
	static_dir = ""

	def __init__(self, host=None, user=None, password=None):
		if host is not None:
			self.host = host
			self.user = user
			self.password = password
		elif EasyFTP.static_host != "":
			self.host = EasyFTP.static_host
			self.user = EasyFTP.static_user
			self.password = EasyFTP.static_password

	@staticmethod
	def build_from_static():
		if EasyFTP.static_host == "":
			config_server = ConfigServer("petMe")
			required_values = [
				"ftp_host",
				"ftp_user",
				"ftp_password",
				"ftp_dir"
			]
			results = config_server.patch(required_values).json()

			EasyFTP.static_host = results["ftp_host"]
			EasyFTP.static_user = results["ftp_user"]
			EasyFTP.static_password = results["ftp_password"]
			EasyFTP.static_dir = results["ftp_dir"]
		connection = EasyFTP()
		connection.host = EasyFTP.static_host
		connection.user = EasyFTP.static_user
		connection.password = EasyFTP.static_password
		return connection

	def connect(self) -> FTP:
		self.connection = FTP(self.host)
		self.connection.login(self.user, self.password, "noaccount")
		return self.connection

	def close(self):
		self.connection.close()

	def set_dir(self, path: str = None) -> bool:
		changed = False
		if path is not None:
			try:
				self.connection.cwd(path)
				changed = True
			except error_perm:
				changed = False
		elif path is not None and EasyFTP.static_dir != "":
			try:
				self.connection.cwd(EasyFTP.static_dir)
				changed = True
			except error_perm:
				changed = False
		return changed

	def upload_binary(self, file_obj, new_name: str, from_local: bool = True) -> bool:
		command: str = f"STOR {new_name}"
		result_code: str
		if from_local:
			with open(file_obj, "rb") as upload_file:
				result_code = self.connection.storbinary(command, upload_file).split(" ")[0]
		else:
			result_code = self.connection.storbinary(command, file_obj).split(" ")[0]
		return result_code == "226"
