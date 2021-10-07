from src.model.Persona import Persona


class Adoptante(Persona):
	def __init__(self):
		super().__init__()
		self.id_adoptante = None
		self.vivienda = None

	def login(self) -> bool:
		logeado: bool = False
		if self.email is not None and self.password is not None:
			query = "SELECT COUNT(*) AS TOTAL FROM Adoptante " \
			        "INNER JOIN Persona ON Adoptante.id_adoptante = Persona.id_persona " \
			        "WHERE correo_electronico = %s AND contrasena = %s"
			valores = [self.email, self.password]
			logeado = self.conexion.select(query, valores)[0]["TOTAL"] == 1
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
