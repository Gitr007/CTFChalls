import bson
import os, base64, zlib, random
from bson import BSONCoding, import_class

class Member(BSONCoding):
    def __init__(self, username = "", code = "00", password = ""):
        self.username = username
        self.code = code
        self.password = password
    
    def __str__(self):
        display = "Username : \nCode : \nPassword : "
        if isinstance(self.username, basestring) and isinstance(self.code, basestring) and isinstance(self.password, basestring):
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
        if isinstance(self.filename, basestring) and (self.filename.__eq__('oold_flag.py') or self.filename.__eq__('new_flag.py')):
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


# import serpy, json, os
# import random, pickle, base64

# class Member(object):
#     username = ""
#     code = 0
#     password = ""

#     def __init__(self, username = "", code = 0, password = ""):
#         self.username = username
#         self.code = code
#         self.password = password

#     def __str__(self):
#         display = "Username : " + self.username + "\nCode : " + str(self.code) + "\nPassword : " + self.password 
#         return display

# class FileReader(object):
#     _id = 0
#     filename = ""

#     def __init__(self, file_name):
#         self.filename = file_name
#         self._id = random.randint(0, 2000)
    
#     def __str__(self):
# 	 if self.filename in ["utils/oold_flag.py", "utils/new_flag.py"]:
#          	return "File Id: " + str(self._id) + "\n==========================================\n" + open(self.filename).read()
# 	 else:
# 		return "File Id: " + str(self._id) + "\n==========================================\n"

# class FileReaderSerializer(serpy.Serializer):
#     Id = serpy.Field(attr="_id")
#     filename = serpy.Field(attr="filename")
#     file = serpy.MethodField()
    
#     def get_file(self, obj):
#         return obj.__str__()

# class MemberSerializer(serpy.Serializer):
#     username = serpy.Field(attr='username')
#     code = serpy.Field(attr='code')
#     password = serpy.Field(attr='password')
#     member = serpy.MethodField()

#     def get_member(self, obj):
#         return obj.__str__()

