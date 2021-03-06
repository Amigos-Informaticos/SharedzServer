from src.connection.EasyConnection import EasyConnection
from src.connection.EasyFTP import EasyFTP
from src.model.Persona import Persona
from src.routes.HTTPStatus import BAD_REQUEST, CONFLICT, FILE_UPLOADED, INTERNAL_SERVER_ERROR, \
	NOT_ACCEPTABLE, \
	NOT_FOUND, NO_CONTENT, OK, \
	RESOURCE_CREATED


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
			resultado = self.conexion.select(query, valores)
			if resultado[0]["TOTAL"] == 1:
				logeado = OK
			else:
				logeado = NOT_FOUND
		return logeado

	def guardar(self) -> int:
		estado: int = BAD_REQUEST
		if self.nombre is not None and not self.esta_registrado():
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
				estado = RESOURCE_CREATED
			else:
				estado = CONFLICT
		else:
			estado = CONFLICT
		return estado

	def actualizar(self) -> int:
		estado: int = BAD_REQUEST
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
			estado = NOT_FOUND
			if self.conexion.send_query(query, valores):
				estado = OK
		return estado

	def eliminar(self) -> int:
		estado: int = BAD_REQUEST
		if self.id_adoptante is not None:
			if self.cargar_adoptante():
				query = "CALL SPE_eliminarAdoptante(%s)"
				valores = [self.id_adoptante]
				if self.conexion.send_query(query, valores):
					estado = OK
				else:
					estado = NOT_ACCEPTABLE
			else:
				estado = NOT_FOUND
		return estado

	def esta_registrado(self):
		registrado = False
		if self.email is not None:
			query = "SELECT COUNT(*) AS TOTAL FROM Persona WHERE email = %s"
			valores = [self.email]
			registrado = self.conexion.select(query, valores)[0]["TOTAL"] == 1
		return registrado

	def cargar_adoptante(self) -> bool:
		cargado = False
		if self.id_adoptante is not None or self.email is not None:
			query = "CALL SPS_obtenerAdoptante(%s, %s)"
			valores = [self.id_adoptante, self.email]
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
				if atributo == "password":
					self.set_password(valores[atributo])
				else:
					self.__setattr__(atributo, valores[atributo])
				cargado = True
		return cargado

	def jsonificar(self, valores_deseados=None) -> dict:
		diccionario = {"id_persona": self.id_adoptante}
		if valores_deseados is not None:
			for atributo in self.__dict__:
				if atributo in valores_deseados:
					diccionario[atributo] = self.__getattribute__(atributo)
		else:
			for atributo in self.__dict__:
				if atributo != "id_adoptante" and atributo != "conexion":
					if atributo == "fecha_nacimiento":
						diccionario[atributo] = str(self.fecha_nacimiento)
					else:
						diccionario[atributo] = self.__getattribute__(atributo)
		return diccionario

	def solicitar_adopcion(self, id_mascota: int) -> tuple:
		id_solicitud = 0
		estado = BAD_REQUEST
		if self.id_adoptante is not None and id_mascota is not None:
			query = 'CALL SPI_registrarSolicitud(%s, %s)'
			valores = [id_mascota, self.id_adoptante]
			resultado = self.conexion.select(query, valores)
			if resultado:
				id_solicitud = resultado[0]["id_solicitud"]
				estado = RESOURCE_CREATED
			else:
				estado = CONFLICT
		return estado, id_solicitud

	def obtener_solicitudes(self):
		solicitudes: list = []
		if self.id_adoptante is not None:
			query = "SELECT * FROM Solicitud WHERE persona = %s"
			valores = [self.id_adoptante]
			resultados = self.conexion.select(query, valores)
			if resultados:
				solicitudes = resultados
		return solicitudes

	def eliminar_solicitud(self, id_mascota):
		estado = BAD_REQUEST
		if self.id_adoptante is not None:
			query = "DELETE FROM Solicitud WHERE persona = %s AND mascota = %s"
			valores = [self.id_adoptante, id_mascota]
			estado = INTERNAL_SERVER_ERROR
			if self.conexion.send_query(query, valores):
				estado = OK
		return estado

	@staticmethod
	def obtener_todas_solicitudes():
		solicitudes: list = []
		conexion = EasyConnection.build_from_static()
		query = "SELECT * FROM Solicitud"
		resultados = conexion.select(query)
		if resultados:
			solicitudes = resultados
		return solicitudes

	def guardar_imagen(self, file_obj) -> int:
		estado = NOT_FOUND
		if self.id_adoptante is not None:
			url = f"https://amigosinformaticos.ddns.net:42070/adoptantes/{self.id_adoptante}/imagen"
			path = f"p_{self.id_adoptante}.png"
			ftp_con = EasyFTP.build_from_static()
			ftp_con.connect()
			ftp_con.set_dir("pet_me_images")
			estado = INTERNAL_SERVER_ERROR

			if ftp_con.upload_binary(file_obj, path, False):
				query = "UPDATE Persona SET imagen = %s WHERE id_persona = %s"
				valores = [url, self.id_adoptante]

				if self.conexion.send_query(query, valores):
					estado = FILE_UPLOADED
			ftp_con.close()
		return estado

	def obtener_imagen(self) -> tuple:
		respuesta = (NOT_FOUND, None)
		if self.id_adoptante is not None:
			respuesta = (NO_CONTENT, None)
			query = "SELECT COUNT(*) AS TOTAL FROM Persona WHERE id_persona = %s AND imagen IS NOT NULL"
			valores = [self.id_adoptante]
			resultado = self.conexion.select(query, valores)[0]["TOTAL"]

			if resultado > 0:
				path = f"p_{self.id_adoptante}.png"
				ftp_con = EasyFTP.build_from_static()
				ftp_con.connect()
				ftp_con.set_dir("pet_me_images")
				downloaded_file = ftp_con.download_binary(path)
				ftp_con.close()
				respuesta = (OK, downloaded_file)
		return respuesta

	def eliminar_imagen(self) -> int:
		respuesta = NOT_FOUND
		if self.id_adoptante is not None:
			query = 'UPDATE Persona SET imagen = NULL WHERE id_persona = %s'
			valores = [self.id_adoptante]
			if self.conexion.send_query(query, valores):
				respuesta = OK
		return respuesta
