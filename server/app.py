#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API",
        }
        return make_response(response_dict, 200)

api.add_resource(Home, '/')

class Newsletters(Resource):
    def get(self):
        newsletters = Newsletter.query.all()
        response = [n.to_dict() for n in newsletters]
        return make_response(response, 200)

    def post(self):
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )
        db.session.add(new_record)
        db.session.commit()
        return make_response(new_record.to_dict(), 201)

api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):
    def get(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return make_response({"error": "Newsletter not found"}, 404)
        return make_response(record.to_dict(), 200)

    def patch(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return make_response({"error": "Newsletter not found"}, 404)

        for attr in request.form:
            setattr(record, attr, request.form[attr])

        db.session.add(record)
        db.session.commit()
        return make_response(record.to_dict(), 200)

    def delete(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return make_response({"error": "Newsletter not found"}, 404)

        db.session.delete(record)
        db.session.commit()
        return make_response({"message": "record successfully deleted"}, 200)

api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
