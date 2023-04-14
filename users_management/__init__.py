from fastapi import HTTPException
from exception_handler import *
from v1.serializers import *
from v1.models import *



def check_user(data: checkUserLogin):
    try:
        # Fetching of data based on email id as well as using fetchUserdetail as an object for decrypting password rather than sending useInsertObject = userInsert() as it is sending blank data.
        fetchUserdetail = userInsert.objects.get(email=data.email)
        # userInsertObject = userInsert()
        decrypt_pass = fetchUserdetail.check_password(pwd = data.password)
        print(decrypt_pass)
        if fetchUserdetail.email == data.email and fetchUserdetail.password == decrypt_pass:
            return True
        return False
    except CustomExceptionHandler as e:
        raise HTTPException(status_code=e.code, detail=e.message)