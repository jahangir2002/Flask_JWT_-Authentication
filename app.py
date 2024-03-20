from flask import Flask, request
from flask_sqlalchemy  import SQLAlchemy
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity


app = Flask(__name__)

app.config['SECRET_KEY'] = 'MY-SECRET-KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///authentic.db'

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)



class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class UserResources(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if not username or not password:
            return {"Message": "Missing Username or Password "}
        if User.query.filter_by(username=username).first():
            return {"Message": "Username already exist"}
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {"Message": "User has been created successfully"}
    
class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()


        if user and user.password==password:
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
            print(access_token)
        
        return {"Message": "Invalid credentials"}
    

class Protected(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return {"Message": f"Hello user {current_user_id} you access the protected resources"}
    
api.add_resource(UserResources, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Protected, '/secure')


if __name__ == "__main__":
    app.run(debug=True)