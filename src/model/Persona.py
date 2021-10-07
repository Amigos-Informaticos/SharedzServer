from abc import ABC, abstractmethod

from src.connection.EasyConnection import EasyConnection


class Persona(ABC):
	def __init__(self):
		self.nombre = None
		self.apellido_paterno = None
		self.apellido_materno = None
		self.telefono = None
		self.fecha_nacimiento = None
		self.sexo = False
		self.localidad = 1
		self.estado = 1
		self.email = None
		self.password = None
		self.conexion = EasyConnection.build_from_static()

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
