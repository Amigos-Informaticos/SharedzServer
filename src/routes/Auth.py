from datetime import datetime
from functools import update_wrapper

from cryptography.fernet import Fernet
from flask import Response, request, session

from src.model.Persona import Persona
from src.routes.HTTPStatus import FORBIDDEN, SESSION_EXPIRED, UNAUTHORIZED
from src.util.Util import decode, encode


class Auth:
	secret_password: bytes = None

	@staticmethod
	def set_password():
		Auth.secret_password = Fernet.generate_key()

	@staticmethod
	def requires_token(operation):
		def verify_auth(*args, **kwargs):
			token = request.headers.get("Token")
			saved_token = None
			try:
				saved_token = session["token"]
				if token is not None and saved_token is not None and token == saved_token:
					session.modified = True
					response = operation(*args, **kwargs)
				else:
					response = Response(status=UNAUTHORIZED)
			except KeyError:
				if token is not None and saved_token is None:
					response = Response(status=SESSION_EXPIRED)
				else:
					response = Response(status=UNAUTHORIZED)
			return response

		return update_wrapper(verify_auth, operation)

	@staticmethod
	def requires_role(role: str):
		def decorator(operation):
			def verify_role(*args, **kwargs):
				token = request.headers.get("Token")
				if token is not None:
					values = Auth.decode_token(token)
					if str(values["is_owner"]) == str(role):
						response = operation(*args, **kwargs)
					else:
						response = Response(status=FORBIDDEN)
				else:
					response = Response(status=FORBIDDEN)
				return response

			return update_wrapper(verify_role, operation)

		return decorator

	@staticmethod
	def generate_token(user: Persona) -> str:
		if Auth.secret_password is None:
			Auth.set_password()
		timestamp = datetime.now().strftime("%H:%M:%S")
		value: str = user.email + "/"
		value += user.password + "/"
		value += timestamp
		return encode(value, Auth.secret_password)

	@staticmethod
	def decode_token(token: str) -> dict:
		decoded_token = decode(token, Auth.secret_password)
		decoded_token = decoded_token.split("/")
		return {
			"email": decoded_token[0],
			"password": decoded_token[1]
		}
