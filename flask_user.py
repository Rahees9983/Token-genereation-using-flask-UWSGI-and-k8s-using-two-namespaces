from flask import Flask, request, jsonify
import pymongo
from flask_restful import Resource, Api, reqparse, abort, inputs
from flask_jwt_extended import(JWTManager, jwt_required, create_access_token, get_jwt_identity)
from passlib.hash import bcrypt
from functools import wraps
from modules import globals as g
# import globals as g


app = Flask(__name__)


def get_http_exception_handler(app):
    """Overrides the default http exception handler to return JSON."""
    handle_http_exception = app.handle_http_exception
    @wraps(handle_http_exception)
    def ret_val(exception):
        exc = handle_http_exception(exception)
        return jsonify({'code': exc.code, 'msg': exc.description}), exc.code
    return ret_val

# Override the HTTP exception handler.
app.handle_http_exception = get_http_exception_handler(app)

app.config['JWT_SECRET_KEY'] = g.SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = g.ACCESS_TOKEN_EXPIRES
app.config['PROPAGATE_EXCEPTIONS'] = True
app.debug = False
jwt = JWTManager(app)


def _get_hash(password):
    return bcrypt.hash(password)


def check_credentials(username,supplied_password):
    # stored_password_hash = user_object.get('password')
    usr_name, usr_pass = get_user(username)
    stored_password_hash = usr_pass
    if not bcrypt.verify(supplied_password, stored_password_hash):
        print("Hashes do NOT match")
        return False
    else:
        print('Hashes are correct')
        return True


def get_user(user):
    # return self.users.get(self.query.name == user)
    # conn = pymongo.MongoClient()    # use this while running on local
    # conn = pymongo.MongoClient("mongodb://jwt-mongo-service")
    # conn = pymongo.MongoClient("mongodb://mongoservice")
    conn = pymongo.MongoClient('mongodb://mongoservice.mydbnamespace')

    res= conn["uwsgi_user"]["uwsgi_user_data"].find({"usr_name_key":user})
    usr_name =""
    usr_pass=""
    for i in res:
        # list(usr_name) = i.values()
        list1 = list(i.items()) 
        print("List is ",list1)
        usr_name = list1[1][1]
        usr_pass = list1[2][1]
    print("######################  ",usr_name,"   ",usr_pass)

    return usr_name, usr_pass



@app.route("/add_usr_name_and_usr_pass",methods=['POST'])
def user_add():
    # conn = pymongo.MongoClient("mongodb://jwt-mongo-service")
    # conn = pymongo.MongoClient("mongodb://mongoservice")
    # conn = pymongo.MongoClient()
    conn = pymongo.MongoClient('mongodb://mongoservice.mydbnamespace')
    
    usr_name = request.get_json()["usr_name_key"]
    usr_pass = _get_hash(request.get_json()["usr_pass_key"])
    usr_obj = {"usr_name_key":usr_name,"usr_pass":usr_pass}
    print("the value of usr_name_key ",usr_name)
    print("the value of usr_pass_key ",usr_pass)

    user = conn["uwsgi_user"]["uwsgi_user_data"].insert_one(usr_obj)
    return "User added successfully"


@app.route("/login",methods=["POST"])
def login():
    print("Inside the login Route +++++++++++++++++++++++++")
    for_check_from_postman_usrname = request.get_json()["usr_name_key"]
    for_check_from_postman_usrpass = request.get_json()["usr_pass_key"]
    print("Afert the postman  ")

    if not for_check_from_postman_usrname:
        abort(400, message='Missing username')
    if not for_check_from_postman_usrpass:
        abort(400, message='Missing password')
    if not check_credentials(for_check_from_postman_usrname,for_check_from_postman_usrpass):
        abort(401, message='incorrect credentials')
    
    access_token = create_access_token(identity=for_check_from_postman_usrname)
    response = jsonify(access_token=access_token, expires=g.ACCESS_TOKEN_EXPIRES)
    response.status_code = 200
    print("Rahees this is ur jwt_token ",response.data)
    # return response
    return "You are a valid user and You can procced further and your token is genetrated \n "

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")




# File "/usr/local/lib/python3.6/site-packages/pymongo/topology.py", line 485, in get_server_session
#     None)
#   File "/usr/local/lib/python3.6/site-packages/pymongo/topology.py", line 209, in _select_servers_loop
#     self._error_message(selector))
# pymongo.errors.ServerSelectionTimeoutError: jwt-mongo-service:27017: [Errno -2] Name or service not known
# [pid: 1|app: 0|req: 1/1] 192.168.99.1 () {40 vars in 726 bytes} [Wed Feb 19 11:04:59 2020] POST
#  /add_usr_name_and_usr_pass 0428 msecs (HTTP/1.1 500) 0 headers in 0 bytes (0 switches on core 0)