from src.model.SQLEntity import SQLEntity
from src.routes.HTTPStatus import BAD_REQUEST, NOT_FOUND, OK, RESOURCE_CREATED
from src.util.Util import md5


class Miembro(SQLEntity):
	def __init__(self):
		super(Miembro, self).__init__()
		self.id_miembro = None
		self.nombre = None
		self.email = None
		self.password = None

	def set_password(self, password: str) -> None:
		self.password = md5(password)

	def registrar(self) -> int:
		estado: int = BAD_REQUEST
		if self.nombre is not None and self.email is not None and self.password is not None:
			query: str = "CALL SPI_registrarMiembro(%s, %s, %s)"
			valores: list = [self.nombre, self.email, self.password]
			resultado: dict = self.conexion.select(query, valores)
			if resultado:
				self.id_miembro = resultado[0]["id_miembro"]
				estado = RESOURCE_CREATED
		return estado

	def login(self) -> int:
		estado: int = BAD_REQUEST
		if self.email is not None and self.password is not None:
			query: str = "SELECT COUNT(*) AS TOTAL FROM Miembro " \
			             "WHERE email = %s AND password = %s"
			valores: list = [self.email, self.password]
			if self.conexion.select(query, valores)[0]["TOTAL"] == 1:
				estado = OK
			else:
				estado = NOT_FOUND
		return estado

	def cargar(self) -> bool:
		cargado: bool = False
		if self.id_miembro is not None or self.email is not None:
			query: str = "CALL SPS_obtenerMiembro(%s, %s)"
			valores: list = [self.id_miembro, self.email]
			resultados = self.conexion.select(query, valores)
			if resultados:
				resultado = resultados[0]
				for atributo in self.atributos_vigilados():
					if atributo in resultado:
						self.__setattr__(atributo, resultado[atributo])
				cargado = True
		return cargado

	def cargar_de_json(self, values: dict) -> bool:
		cargado: bool = False
		for atributo in self.__dict__:
			if atributo in values:
				if atributo == "password":
					self.set_password(values[atributo])
				else:
					self.__setattr__(atributo, values[atributo])
				cargado = True
		return cargado

	def jsonificar(self, valores_requeridos=None) -> dict:
		diccionario: dict = {"id_miembro": self.id_miembro}
		if valores_requeridos is not None:
			for atributo in self.atributos_vigilados():
				if atributo in valores_requeridos:
					diccionario[atributo] = self.__getattribute__(atributo)
		else:
			for atributo in self.atributos_vigilados():
				diccionario[atributo] = self.__getattribute__(atributo)
		return diccionario
