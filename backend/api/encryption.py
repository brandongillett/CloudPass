from cryptography.fernet import Fernet
from .config import db
from .auth import verify_password
import hashlib
import base64

def genFernetKey(password):
    password_bytes = password.encode('utf-8')
    salt = b'PasswordManager'
    salted_password = password_bytes + salt
    key = salted_password
    for _ in range(1000000):
        key = hashlib.sha256(key).digest()
    encoded_key = base64.urlsafe_b64encode(key[:32])
    return encoded_key

def encrypt_password(key, data):
    fernet = Fernet(key)
    for key,val in data.items():
        data[key] = fernet.encrypt(val.encode())
    return data

def decrypt_passwords(key,passwords):
    fernet = Fernet(key)
    decrypted = []
    for password in passwords:
        for elem,enc in password.items():
            if elem != 'id':
                password[elem] = fernet.decrypt(enc)
        decrypted.append(password)
    return decrypted

def new_password(user: str,fernetKey: str,service: str,username: str,password: str,notes: str):
    if not service or not username or not password:
        return {"status":False,"message":"Service name required."} if not service else {"status":False,"message":"Username required."} if not username else {"status":False,"message":"Password required."}
    try:
        data = encrypt_password(fernetKey,{'service':service,'username':username,'password':password,'notes':notes})
        cursor = db.cursor()
        cursor.execute('INSERT INTO Passwords (userId,service,username,password,notes) VALUES (%s,%s,%s,%s,%s)',(user.id,data['service'],data['username'],data['password'],data['notes']))
        cursor.close()
        db.commit()
        return {"status":True,"message":f"Password Saved."}
    except:
        return {"status":False,"message":"An error has occured."}

def edit_password(user: str,passId,fernetKey: str,service: str,username: str,password: str,notes: str):
    cursor = db.cursor()
    cursor.execute(f'Select userId FROM Passwords WHERE userId="{user.id}" AND id="{passId}"')
    userId=cursor.fetchone()
    if(userId and user.id == userId[0]):
        try:
            data = encrypt_password(fernetKey,{'service':service,'username':username,'password':password,'notes':notes})
            cursor.execute('UPDATE Passwords SET service="%s", username="%s", password="%s", notes="%s" WHERE userId="%s" AND id="%s"',(data['service'],data['username'],data['password'],data['notes'],user.id,passId))
            cursor.close()
            db.commit()
            return {"status":True,"message":f"Password Saved."}
        except:
            return {"status":False,"message":"An error has occured."}
    else:
        return {"status":False,"message":"Unable to retreive password."}

def get_passwords(user: str,fernetKey: str):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Passwords WHERE userId="{}"'.format(user.id))
    info=cursor.fetchall()
    cursor.close()
    passwords = []
    if info:
        for i in info:
            passwords.append({'id':i[1],'service':i[2],'username':i[3],'password':i[4],'notes':i[5]})
        data = decrypt_passwords(fernetKey,passwords)
        return data
    
def del_password(user: str,passId):
    cursor = db.cursor()
    cursor.execute(f'Select userId FROM Passwords WHERE userId="{user.id}" AND id="{passId}"')
    userId=cursor.fetchone()
    if(userId and user.id == userId[0]):
        try:
            cursor.execute(f'Delete FROM Passwords WHERE userId="{user.id}" AND id="{passId}"')
            cursor.close()
            db.commit()
            return {"status":True,"message":f"Password Deleted."}
        except:
            return {"status":False,"message":"An error has occured."}
    else:
        return {"status":False,"message":"Unable to retreive password."}