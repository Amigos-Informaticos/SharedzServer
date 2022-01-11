from src.model.Miembro import Miembro
from src.model.SQLEntity import SQLEntity
from src.util.Util import md5


class Casa(SQLEntity):
	def __init__(self):
		super(Casa, self).__init__()
		self.id_casa = None
		self.miembros: list = []
		self.nombre = None
		self.codigo_publico = None

	def registrar(self, creador: Miembro) -> bool:
		registrada: bool = False
		if self.nombre is not None:
			self.codigo_publico = md5(self.nombre)[0:10]
		else:
			self.codigo_publico = md5(str(creador.id_miembro))[0:10]
		query: str = "CALL SPI_registrarCasa(%s, %s)"
		valores: list = [self.nombre, self.codigo_publico]
		resultado: list = self.conexion.select(query, valores)
		if resultado:
			self.id_casa = resultado[0]["id_casa"]
			self.agregar_miembro(creador)
			registrada = True
		return registrada

	def agregar_miembro(self, miembro: Miembro) -> bool:
		agregado: bool = False
		if self.id_casa is not None:
			query: str = "CALL SPI_agregarMiembro(%s, %s)"
			valores: list = [self.id_casa, miembro.id_miembro]
			if self.conexion.select(query, valores)[0]["RESULT"] == 1:
				if miembro not in self.miembros:
					self.miembros.append(miembro)
				agregado = True
		return agregado

	def obtener_miembros(self) -> list:
		miembros: list = []
		if self.id_casa is not None or self.codigo_publico is not None:
			query: str = "CALL SPS_obtenerMiembros(%s, %s)"
			valores: list = [self.id_casa, self.codigo_publico]
			resultados: list = self.conexion.select(query, valores)
			if resultados:
				for informacion_miembro in resultados:
					miembro_aux = Miembro()
					miembro_aux.cargar_de_json(informacion_miembro)
					miembros.append(miembro_aux)
		return miembros

	def cargar_miembros(self):
		self.miembros = self.obtener_miembros()

	def eliminar_miembro(self, miembro: Miembro) -> bool:
		eliminado: bool = False
		if self.id_casa is not None:
			query: str = "DELETE FROM MiembrosCasa WHERE id_casa = %s AND id_miembro = %s"
			valores: list = [self.id_casa, miembro.id_miembro]
			if self.conexion.send_query(query, valores):
				if miembro in self.miembros:
					self.miembros.remove(miembro)
				eliminado = True
		return eliminado

	def jsonificar(self, valores_requeridos=None) -> dict:
		diccionario: dict = {"id_casa": self.id_casa}
		if valores_requeridos is not None:
			for atributo in self.atributos_vigilados():
				if atributo in valores_requeridos:
					if atributo == "miembros":
						miembros = []
						for miembro in self.miembros:
							miembros.append(miembro.jsonificar())
						diccionario["miembros"] = miembros
					else:
						diccionario[atributo] = self.__getattribute__(atributo)
		else:
			for atributo in self.atributos_vigilados():
				if atributo == "miembros":
					miembros = []
					for miembro in self.miembros:
						miembros.append(miembro.jsonificar())
					diccionario["miembros"] = miembros
				else:
					diccionario[atributo] = self.__getattribute__(atributo)
		return diccionario
