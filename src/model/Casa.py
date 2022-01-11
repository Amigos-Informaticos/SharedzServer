from src.model.Miembro import Miembro
from src.model.SQLEntity import SQLEntity


class Casa(SQLEntity):
	def __init__(self):
		super(Casa, self).__init__()
		self.id_casa = None
		self.miembros: list = []
		self.codigo_publico = None

	def agregar_miembro(self, miembro: Miembro) -> bool:
		agregado: bool = False
		if miembro not in self.miembros:
			self.miembros.append(miembro)
			agregado = True
		return agregado

