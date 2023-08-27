from cryptography.fernet import Fernet


def decrypt(key, passward):
    '''
    password를 복호화한다.
    '''
    
    f = Fernet(key)
    return f.decrypt(passward).decode()
    
def encrypt(key,passward):
    '''
    password를 암호화한다.
    '''
    
    f = Fernet(key)
    return f.encrypt(passward.encode()).decode()
