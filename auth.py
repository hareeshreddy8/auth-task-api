from passlib.context import CryptContext

#using passlib to hash the password(oneway)
pwd_context = CryptContext(schemes= ["bcrypt"],deprecated = "auto")

def hashing_password(password):
    print("PASSWORD LENGTH:", len(password.encode("utf-8")))
    return pwd_context.hash(password)


#signinup user
def signup_user(username,password,all_usernames,database_insertuser):
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
    
    usernames = [u[0] for u in all_usernames()]
    if username in usernames:
        return None,("Username already exists",400)
    
    password = hashing_password(password)
    if not password:
        return None,("invalid password",400)
    
    user_details = database_insertuser(username,password)
    
    return user_details,None


def login_user(username,password,get_user_details):

    user_details = get_user_details(username)

    if not user_details:
        return {
            "msg":"Invalid credentials. "
            }
    
    password_hash = user_details.get("password",0)

    if pwd_context.verify(password,password_hash):
        return {
            "msg": "login successfull. "
        }
    
    else:
        return {
            "msg":"Invalid credentials. "
            } 

