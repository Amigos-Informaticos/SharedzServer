from src.model.Adoptante import Adoptante

adoptante = Adoptante()
adoptante.nombre = "Miguel Joaquin"


def test_guardar():
	assert adoptante.guardar() == True
	assert adoptante.id_adoptante is not None


def test_actualizar():
	adoptante.email = "miguel@correo.com"
	adoptante.password = "contraChida"
	assert adoptante.actualizar() == True


def test_login():
	assert adoptante.login() == True


def test_eliminar():
	assert adoptante.eliminar() == True
