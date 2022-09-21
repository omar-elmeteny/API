import json
import flask
from flask import Flask, jsonify, render_template, request, redirect, url_for
from jinja2 import Environment, FileSystemLoader
import os
import webbrowser
from flask_restful import Resource, Api
import logging

logging.basicConfig(filename='contacts.log' , level=logging.DEBUG , 
format='%(asctime)s : %(name)s : %(levelname)s : %(message)s')


app = flask.Flask(__name__, template_folder='templates')
app.config["DEBUG"]
api = Api(app)

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment(loader=FileSystemLoader(templates_dir))
#template = env.get_template('contacts.html')


logging.info("Serving Flask app 'contacts'")
logging.info("Debug mode: off")
logging.warning("This is a development server. Do not use it in a production deployment. Use a production WSGI server instead")
logging.info("Running on http://127.0.0.1:5000")

@app.errorhandler(404)
def error_page(e):
	url = request.base_url
	logging.error("Page not found, " + url + " is a wrong url 400-")
	return "<h1>Page Not Found</h1>", 404


@app.route('/', methods=['GET'])
def home():
	logging.info("Running on http://127.0.0.1:5000/ (Homepage) 200-")
	return "<h1>Hello World!</h1>"


contacts = {}


# @app.route('/contacts/all', methods=['GET'])
# def cont_all():
#     with open('\API\contacts.json', 'r') as f:
#         contacts = json.load(f)
#     return render_template("contacts.html", result=contacts)


# @app.route('/contacts', methods=['GET', 'POST'])
# def cont_one():
#     if request.method == 'POST':
#         contact = request.form
#         c = {
#             "id": int(contact["id"]),
#             "fname": contact["fname"],
#             "lname": contact["lname"],
#             "number": contact["number"]
#         }
#         with open('\API\contacts.json', 'r') as f:
#             contacts = json.load(f)
#         contacts.append(c)
#         with open('\API\contacts.json', 'w') as f:
#             json.dump(contacts, f)
#         return redirect(url_for("cont_all"))
#     else:
#         ids = request.args.getlist("id")
#         if id == None:
#             return "<h1>No ID specified</h1>"
#         else:
#             result = []
#             with open('\API\contacts.json', 'r') as f:
#                 contacts = json.load(f)
#             for contact in contacts:
#                 if ids.__contains__(str(contact["id"])):
#                     result.append(contact)
#             return render_template("contacts.html", result=result)


class Contacts(Resource) :
	def get(self, id):
		logging.debug("ID = " + str(id))
		if id == "all" :
			logging.info("Running on http://127.0.0.1:5000/contacts/all (All Contacts Page) 200-")
		elif int(id) >= 0:
			logging.info("Running on http://127.0.0.1:5000/contacts/" + id + " (One Contact Page) 200-")    
		with open('\API\contacts.json', 'r') as f:
			contacts = json.load(f)
			logging.debug("Contacts = " + str(contacts))
		if id == "all" :
			return contacts	
		for contact in contacts :
			logging.debug("Contact = " + str(contact))      
			if contact["id"] == int(id):
				logging.debug("Result = " + str(contact)) 
				return contact
		return None		 

	def post(self, id):
		contact = request.form
		c = {
			"id" : int(id),
			"fname" : contact["fname"],
			"lname" : contact["lname"],
			"number" : contact["number"]
		}
		with open('\API\contacts.json', 'r') as f:
			contacts = json.load(f)
		i = 0
		flag = False
		while i < len(contacts) :
			contact = contacts[i]
			if contact["id"] == c["id"] :
				contacts[i] = c
				flag = True
				break
			i = i + 1
		if not flag :
			contacts.append(c)
		with open('\API\contacts.json', 'w') as f:
			json.dump(contacts, f, indent=4)	
		return c

api.add_resource(Contacts, '/contacts/<string:id>')

@app.errorhandler(500)
def error_page(e):
	url = request.base_url
	logging.error("ID is out of range, " + url + " caused an internal server error 500-")
	return "<h1>ID out of range</h1>", 500


app.run()
