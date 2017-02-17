from models import Base, User
from flask import Flask, jsonify, request, url_for, abort
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

engine = create_engine('sqlite:///users.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/api/users', methods = ['POST', 'GET'])
def new_user():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        
        if username is None or password is None:
            abort(400)
        if session.query(User).filter_by(username = username).first() is not None:
            abort(400)

        user = User(username = username)
        user.hash_password(password)
        print (user.password_hash)

        session.add(user)
        session.commit()    
        return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id = user.id, _external = True)}
    elif request.method == 'GET':
        users = session.query(User).all()
        return jsonify(users = [i.username for i in users])
        
@app.route('/api/users/<int:id>')
def get_user(id):
    try:
        user = session.query(User).filter_by(id=id).one()
        if not user:
            abort(400)
    except MultipleResultsFound, e:
        print e
        abort(400)
    except NoResultFound, e:
        print e
        abort(400)

    return jsonify({'username': user.username})
    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
