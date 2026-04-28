from passlib.context import CryptContext

pwd_context = CryptContext(schemes= ["bcrypt"],deprecated = "auto")
def hashing_password(password):
    print("PASSWORD LENGTH:", len(password.encode("utf-8")))
    return pwd_context.hash(password)

def signup_user(username,password,all_usernames,database_insertuser):
    print("SIGNUP FUNCTION EXECUTED")
    if len(password.encode("utf-8")) > 72:
        return None, ("Password too long (max 72 characters)", 400)
    usernames = [u[0] for u in all_usernames()]

    if username in usernames:
        return None,("Username already exists",400)
    
    password = hashing_password(password)
    if not password:
        return None,("invalid password",400)
    user_details = database_insertuser(username,password)
    return user_details,None
