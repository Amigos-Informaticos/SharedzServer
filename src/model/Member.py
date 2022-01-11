from src.model.SQLEntity import SQLEntity
from src.routes.HTTPStatus import BAD_REQUEST, NOT_FOUND, OK, RESOURCE_CREATED
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

	def register(self) -> int:
		status: int = BAD_REQUEST
		if self.name is not None and self.email is not None and self.password is not None:
			query: str = "CALL SPI_registerMember(%s, %s, %s)"
			values: list = [self.name, self.email, self.password]
			results: dict = self.connection.select(query, values)
			if results:
				self.id_member = results[0]["id_member"]
				status = RESOURCE_CREATED
		return status

	def login(self) -> int:
		status: int = BAD_REQUEST
		if self.email is not None and self.password is not None:
			query: str = "SELECT COUNT(*) AS TOTAL FROM Member " \
			             "WHERE email = %s AND password = %s"
			values: list = [self.email, self.password]
			if self.connection.select(query, values)[0]["TOTAL"] == 1:
				status = OK
			else:
				status = NOT_FOUND
		return status

	def load_member(self) -> bool:
		loaded: bool = False
		if self.id_member is not None or self.email is not None:
			query: str = "CALL SPS_getMember(%s, %s)"
			values: list = [self.id_member, self.email]
			results = self.connection.select(query, values)
			if results:
				result = results[0]
				for attribute in self.watched_attributes():
					if attribute in result:
						self.__setattr__(attribute, result[attribute])
				loaded = True
		return loaded

	def load_from_json(self, values: dict) -> bool:
		loaded: bool = False
		for attribute in self.__dict__:
			if attribute in values:
				if attribute == "password":
					self.set_password(values[attribute])
				else:
					self.__setattr__(attribute, values[attribute])
				loaded = True
		return loaded

	def jsonify(self, required_values=None) -> dict:
		built_object: dict = {"id_member": self.id_member}
		if required_values is not None:
			for attribute in self.watched_attributes():
				if attribute in required_values and attribute not in built_object:
					built_object[attribute] = self.__getattribute__(attribute)
		else:
			for attribute in self.watched_attributes():
				built_object[attribute] = self.__getattribute__(attribute)
		return built_object
