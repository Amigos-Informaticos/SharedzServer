from src.connection.EasyConnection import EasyConnection
from src.routes.HTTPStatus import BAD_REQUEST, CONFLICT, NOT_ACCEPTABLE, NOT_FOUND, OK, \
	RESOURCE_CREATED


class Refugio:
	def __init__(self):
		self.id_refugio = None
		self.nombre = None
		self.estado = None
		self.localidad = None
		self.direccion = None
		self.pagina_web = None
		self.telefono = None
		self.email = None
		self.fundacion = None
		self.conexion = EasyConnection.build_from_static()

	def guardar(self) -> int:
		estado = BAD_REQUEST
		if self.nombre is not None:
			query = "CALL SPI_registrarRefugio(%s, %s, %s, %s, %s, %s, %s, %s)"
			valores = [
				self.nombre,
				self.estado,
				self.localidad,
				self.direccion,
				self.pagina_web,
				self.telefono,
				self.email,
				self.fundacion
			]
			resultado = self.conexion.select(query, valores)
			if resultado:
				self.id_refugio = resultado[0]["_id_refugio"]
				estado = RESOURCE_CREATED
			else:
				estado = CONFLICT
		else:
			estado = NOT_ACCEPTABLE
		return estado

	def actualizar(self) -> int:
		estado = BAD_REQUEST
		if self.id_refugio is not None:
			query = "CALL SPA_actualizarRefugio(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
			valores = [
				self.id_refugio,
				self.nombre,
				self.estado,
				self.localidad,
				self.direccion,
				self.pagina_web,
				self.telefono,
				self.email,
				self.fundacion
			]
			estado = NOT_FOUND
			if self.conexion.send_query(query, valores):
				estado = OK
		return estado

	def cargar(self) -> bool:
		cargado = False
		if self.id_refugio is not None:
			query = "SELECT * FROM Refugio WHERE id_refugio = %s"
			valores = [self.id_refugio]
			resultado = self.conexion.select(query, valores)
			if resultado:
				resultado = resultado[0]
				for atributo in self.__dict__:
					if atributo in resultado:
						self.__setattr__(atributo, resultado[atributo])
				cargado = True
		return cargado

	def cargar_de_json(self, valores: dict) -> bool:
		cargado: bool = False
		for atributo in self.__dict__:
			if atributo in valores:
				self.__setattr__(atributo, valores[atributo])
				cargado = True
		return cargado

	def eliminar(self) -> int:
		estado = BAD_REQUEST
		if self.id_refugio is not None:
			if self.cargar():
				query = "DELETE FROM Refugio WHERE id_refugio = %s"
				valores = [self.id_refugio]
				if self.conexion.send_query(query, valores):
					estado = OK
				else:
					estado = NOT_ACCEPTABLE
			else:
				estado = NOT_FOUND
		return estado

	def jsonificar(self, valores_deseados=None) -> dict:
		diccionario = {}
		if valores_deseados is not None:
			for atributo in self.__dict__:
				if atributo in valores_deseados:
					diccionario[atributo] = self.__getattribute__(atributo)
		else:
			for atributo in self.__dict__:
				if atributo != "conexion":
					diccionario[atributo] = self.__getattribute__(atributo)
		return diccionario
