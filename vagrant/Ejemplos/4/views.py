from models import Base, User
from flask import Flask, request, jsonify, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///users.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user    

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

    g.user = user;
    return jsonify({'username': user.username})
    
@app.route('/api/protected_resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
