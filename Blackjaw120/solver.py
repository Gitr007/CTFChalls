import cPickle, bson
import os, base64, zlib, random
from bson import BSONCoding, import_class
from utils import wmodules as uc

class Member(BSONCoding):
    
    def __init__(self, username = "", code = 0, password = ""):
        
        self.username = username
        self.code = code
        self.password = password
    
    def __str__(self):
        display = "Username : " + str(self.username) + "\nCode : " + str(self.code) + "\nPassword : " + str(self.password) 
        return display

    def bson_encode(self):
        return {"username": self.username, "code": self.code, "password": self.password}

    def bson_init(self, raw_values):
        self.username = raw_values["username"]
        self.code = raw_values["code"]
        self.password = raw_values["password"]
    
    def __eq__(self, other):
        if not isinstance(other, Member):
            return NotImplemented
        if self.username != other.code:
            return False
        if self.code != other.code:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

class FileReader(BSONCoding):

    def __init__(self, file_name):
        self.filename = file_name
        self._id = random.randint(0, 2000)
    
    def __str__(self):
        if self.filename.__eq__('oold_flag.py') or self.filename.__eq__('new_flag.py'):
            fh = open('utils/'+self.filename,'r')
            display = "File Id: " + str(self._id) + \
            "\n==========================================\n" + \
            fh.read()
            fh.close()
            return display
        else:
		    return "File Id: " + str(self._id) + \
            "\n==========================================\n"
    
    def bson_encode(self):
        return {"filename": self.filename, "_id": self._id}

    def bson_init(self, raw_values):
        self.filename = raw_values["filename"]
        self._id = raw_values["_id"]
    
    def __eq__(self, other):
        if not isinstance(other, FileReader):
            return NotImplemented
        if self.filename != other.filename:
            return False
        if self._id != other._id:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

class p:
   def __init__(self):
        return None
   def __str__(self):
       return open("utils/new_flag.py").read()



import_class(uc.FileReader)
# data = FileReader('new_flag.py')



data = uc.FileReader('new_flag.py')

# if type(data) is FileReader:()
#     print "YESS"

serialized = bson.dumps(data)

p =  zlib.compress(serialized).encode('base64')
# p = zlib.compress(bson.dumps({'cls_ob':p.__str__()}))
print p

print zlib.decompress(p.decode('base64'))

# print serialized
# serialized = base64.b64encode(zlib.compress(serialized))

# print serialized

# print zlib.decompress(base64.b64decode(serialized))

print bson.loads(serialized)



# TODO:
# Add compression functions zlib : DONE
# create git repo and zip it : DONE
# Blackjaw folder and docker it: 
# Test securing inputs last check 
# Secure access to files