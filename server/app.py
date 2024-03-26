from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages_dict = [mess.to_dict() for mess in Message.query.order_by('created_at').all()]
        return make_response(messages_dict, 200)
    elif request.method == "POST":
        new_message = Message(
            body = request.json.get("body"),
            username = request.json.get("username")
        )
        db.session.add(new_message)
        db.session.commit()
        return make_response(new_message.to_dict(), 201)

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

if __name__ == '__main__':
    app.run(port=5555)
