from src.model.Persona import Persona
from src.routes.HTTPStatus import BAD_REQUEST, NOT_FOUND, OK


class Adoptante(Persona):
	def __init__(self):
		super().__init__()
		self.id_adoptante = None
		self.vivienda = None

	def login(self) -> int:
		logeado: int = BAD_REQUEST
		if self.email is not None and self.password is not None:
			query = "SELECT COUNT(*) AS TOTAL FROM Adoptante " \
			        "INNER JOIN Persona ON Adoptante.id_adoptante = Persona.id_persona " \
			        "WHERE email = %s AND password = %s"
			valores = [self.email, self.password]
			if self.conexion.select(query, valores)[0]["TOTAL"] == 1:
				logeado = OK
			else:
				logeado = NOT_FOUND
		return logeado

	def guardar(self) -> bool:
		guardado: bool = False
		if self.nombre is not None:
			query = "CALL SPI_registrarAdoptante(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			valores = [
				self.nombre,
				self.apellido_paterno,
				self.apellido_materno,
				self.telefono,
				self.email,
				self.fecha_nacimiento,
				self.sexo,
				self.localidad,
				self.estado,
				self.password,
				self.vivienda
			]
			resultado = self.conexion.select(query, valores)
			if resultado:
				self.id_adoptante = resultado[0]["_id_adoptante"]
				guardado = True
		return guardado

	def actualizar(self) -> bool:
		actualizado: bool = False
		if self.id_adoptante is not None:
			query = "CALL SPA_actualizarAdoptante(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			valores = [
				self.id_adoptante,
				self.nombre,
				self.apellido_paterno,
				self.apellido_materno,
				self.telefono,
				self.email,
				self.fecha_nacimiento,
				self.sexo,
				self.localidad,
				self.estado,
				self.password,
				self.vivienda
			]
			actualizado = self.conexion.send_query(query, valores)
		return actualizado

	def eliminar(self) -> bool:
		eliminado: bool = False
		if self.id_adoptante is not None:
			query = "CALL SPE_eliminarAdoptante(%s)"
			valores = [self.id_adoptante]
			eliminado = self.conexion.send_query(query, valores)
		return eliminado

	def cargar_adoptante(self) -> bool:
		cargado = False
		if self.id_adoptante is not None or self.email is not None:
			query = "CALL SPS_obtenerAdoptante(%s, %s)"
			valores = [self.id_adoptante, self.email]
			resultado = self.conexion.select(query, valores)
			if resultado:
				resultado = resultado[0]
				for atributo in self.__dict__:
					if atributo != "conexion":
						self.__setattr__(atributo, resultado[atributo])
				cargado = True
		return cargado
