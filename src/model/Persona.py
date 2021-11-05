from abc import ABC, abstractmethod

from src.connection.EasyConnection import EasyConnection
from src.util.Util import md5


class Persona(ABC):
	def __init__(self):
		self.nombre = None
		self.apellido_paterno = None
		self.apellido_materno = None
		self.telefono = None
		self.fecha_nacimiento = None
		self.sexo = False
		self.localidad = None
		self.estado = None
		self.email = None
		self.password = None
		self.imagen = None
		self.conexion = EasyConnection.build_from_static()

	def set_password(self, password: str) -> None:
		self.password = md5(password)

	@abstractmethod
	def login(self) -> bool:
		pass

	@abstractmethod
	def guardar(self) -> bool:
		pass

	@abstractmethod
	def actualizar(self) -> bool:
		pass

	@abstractmethod
	def eliminar(self) -> bool:
		pass
