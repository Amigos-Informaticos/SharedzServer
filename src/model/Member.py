from src.model.SQLEntity import SQLEntity
from src.util.Util import md5


class Member(SQLEntity):
	def __init__(self):
		super(Member, self).__init__()
		self.id_member = None
		self.name = None
		self.email = None
		self.password = None

	def set_password(self, password: str) -> None:
		self.password = md5(password)

	def register(self) -> bool:
		registered: bool = False
		if self.name is not None and self.email is not None and self.password is not None:
			query: str = "CALL SPI_registerMember(%s, %s, %s)"
			values: list = [self.name, self.email, self.password]
			results: dict = self.connection.select(query, values)
			if results:
				self.id_member = results[0]["id_member"]
				registered = True
		return registered

	def login(self):
		logged_in: bool = False
		if self.email is not None and self.password is not None:
			query: str = "SELECT COUNT(*) AS TOTAL FROM Member " \
			             "WHERE email = %s AND password = %s"
			values: list = [self.email, self.password]
			logged_in = self.connection.select(query, values)[0]["TOTAL"] == 1
		return logged_in
