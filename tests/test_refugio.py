from src.model.Refugio import Refugio
from src.routes.HTTPStatus import CONFLICT, OK, RESOURCE_CREATED

refugio = Refugio()
refugio.nombre = "Refugio de mascotas #1"


def test_guardar():
	estado = refugio.guardar()
	assert estado == RESOURCE_CREATED or estado == CONFLICT


def test_actualizar():
	assert refugio.id_refugio is not None
	refugio.telefono = "22 91 76 36 87"
	refugio.email = "refugio@mascota.com"
	assert refugio.actualizar() == OK


def test_cargar():
	assert refugio.cargar() == True


def test_eliminar():
	assert refugio.eliminar() == OK
