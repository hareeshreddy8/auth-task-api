from passlib.context import CryptContext
from jose import jwt
from datetime import datetime,timedelta
import database


#using passlib to hash the password(oneway)
pwd_context = CryptContext(schemes= ["bcrypt"],deprecated = "auto")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def decode_token(token:str):
    payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    return payload["user_id"]

def hashing_password(password):
    print("PASSWORD LENGTH:", len(password.encode("utf-8")))
    return pwd_context.hash(password)


#signinup user
def signup_user(username,password):
    # print("SIGNUP FUNCTION EXECUTED")
    
    #passsword must be lesss thand 72 bytes
    if len(password.encode("utf-8")) > 72:
        return None, ("Password too long (max 72 characters)", 400)
    
    username = username.strip()
    if not username :
        return None,("Username cannot be empty. ",400)
    
    if len(username) < 3 :
        return None,("Username is too short(min 3 characters)",400)

    if len(username) > 20 :
        return None,("Username is too long(max 20 characters)",400)
    
    usernames = [u[0] for u in database.users()]
    if username in usernames:
        return None,("Username already exists",400)
    
    password = hashing_password(password)
    if not password:
        return None,("invalid password",400)
    
    user_details = database.insert_user(username,password)
    
    return user_details,None


def login_user(username,password):

    user_details = database.get_user_by_username(username)

    if not user_details:
        return None,("invalid credentials. ",400)
    
    password_hash = user_details.get("password")

    if pwd_context.verify(password,password_hash):
        return user_details.get("id"),None
        
        
    else:
        return None,("invalid credentials. ",400)
    
