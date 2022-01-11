import json

from flask import Blueprint, Response, request, session

from src.model.Member import Member
from src.routes.Auth import Auth
from src.routes.HTTPStatus import OK, RESOURCE_CREATED

member_routes = Blueprint("member_routes", __name__)


@member_routes.post("/login")
@Auth.requires_payload({"email", "password"})
def login():
	json_values = request.json
	member = Member()
	member.email = json_values["email"]
	member.set_password(json_values["password"])
	status = member.login()
	response = Response(status=status)
	if status == OK:
		if member.load_member():
			token = Auth.generate_token(member)
			session.permanent = True
			session["token"] = token
			session["email"] = member.email
			session["password"] = member.password
			response = Response(
				json.dumps({
					"token": token,
					"id": member.id_member
				}),
				status=status,
				mimetype="application/json"
			)
	return response


@member_routes.post("/members")
@Auth.requires_payload({"name", "email", "password"})
def register():
	json_values = request.json
	member = Member()
	member.load_from_json(json_values)
	status = member.register()
	response = Response(status=status)
	if status == RESOURCE_CREATED:
		response = Response(
			json.dumps(member.jsonify()),
			status=status,
			mimetype="application/json"
		)
	return response
