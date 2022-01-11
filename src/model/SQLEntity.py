from src.connection.EasyConnection import EasyConnection


class SQLEntity:
	def __init__(self):
		self.conexion = EasyConnection.build_from_static()
		self.atributos_ignorados = ["atributos_ignorados", "conexion"]

	def ignorar_atributo(self, nombre_atributo: str) -> bool:
		ignorado: bool = False
		if nombre_atributo in self.__dict__:
			self.atributos_ignorados.append(nombre_atributo)
			ignorado = True
		return ignorado

	def remover_ignorado(self, nombre_atributo: str) -> bool:
		removido: bool = False
		if nombre_atributo in self.__dict__ and nombre_atributo in self.atributos_ignorados:
			self.atributos_ignorados.remove(nombre_atributo)
			removido = True
		return removido

	def atributos_vigilados(self) -> list:
		atributos_vigilados: list = []
		for atributo in self.__dict__:
			if atributo not in self.atributos_ignorados:
				atributos_vigilados.append(atributo)
		return atributos_vigilados
