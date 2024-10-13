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

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        results = []
        messages = Message.query.order_by('created_at').all()
        for message in messages:
            results.append(message.to_dict())

        return results    

    elif request.method == 'POST':
        data = request.json
        new_message = Message(
            body = data['body'],
            username = data['username']
            # created_at = data['created_at'],
            # updated_at = data['updated_at']
        )

        db.session.add(new_message)
        db.session.commit()

        return jsonify(new_message.to_dict()), 201
        # return {"message":"message added successfully",
        #         "message" : jsonify(new_message)}, 201
    
       


@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'PATCH':
        data = request.json
        message = Message.query.filter(Message.id == id).first()
        for attr in data:
            setattr(message, attr, data[attr])

        db.session.commit()

        return jsonify(message.to_dict())
        # return {"message": "Message updates succesfully",
        #         "updated_message": message }, 201         


    elif request.method == 'DELETE':
        message = Message.query.filter(Message.id == id).first()
        db.session.delete(message)
        db.session.commit()

        return {"message": "Message deleted successfully",
                "deleted_message": message }, 200





if __name__ == '__main__':
    app.run(port=5555)
