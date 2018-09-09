### !/usr/bin/python
import cherrypy
from cherrypy import log
from cherrypy.lib.static import serve_file
import hashlib, base64, os, sys, time, zlib
from unidecode import unidecode
from utils import wmodules as uc
import bson
from bson import BSONCoding, import_class

# Static params
DIR = os.getcwd()
STATIC_DIR = os.path.join(DIR, 'static')
INPUT_ERROR = "<center><b>Missing or Incorrect Information</b></center>"
AUTH_ERROR = "<center><b>Authentication Error Ref:b6a41b54cff6db54cff6d9704 </b></center>"
MEMBERS_PAGE = open(os.path.join(STATIC_DIR,"members.html")).read()

# Error pages
def error_page_404(status="", message="", traceback="", version=""):
    cherrypy.response.headers["Server"] = "PockerServer"
    return serve_file(os.path.join(STATIC_DIR,"404.html"),"text/html", None)

@cherrypy.tools.register('before_finalize', priority=60)
def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"


def error_page_403(status="", message="", traceback="", version=""):
    cherrypy.response.headers["Server"] = "PockerServer"
    return """<html>
    <head><title>403 Forbidden</title>\
    </head>
    <body bgcolor=white>
    <h1>Forbidden 403</h1>
    <hr>
    <h3><b>Only Authorized Intranet Admin can access this page</b></h3>
    <h3><b>This page is not accessible for the public.</b></h3>
    </body>
    </html>"""

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

def ObjectDeserialize(obj):
    import_class(uc.FileReader)
    import_class(uc.Member)
    print obj
    try:
        return bson.loads(obj)
    except:
        return "None"


def ObjectSerialize(obj):
    if type(obj) is uc.FileReader: import_class(uc.FileReader)
    if type(obj) is uc.Member: import_class(uc.Member)
    return bson.dumps(obj)

# Check cookies signature
def checkSignature(auth, sig):
    print "sig = ",sig
    print "auth = ",hashlib.sha1(auth).hexdigest()
    if(hashlib.sha1(auth).hexdigest() == sig):
        return True
    else:
        return False


class WebServer(object):
    
    # Index page controller
    @cherrypy.expose
    def index(self, **args):
    	cherrypy.response.headers["Server"] = "PockerServer"
        if cherrypy.request.method != "GET":
            print cherrypy.request.params
            raise cherrypy.HTTPRedirect("/", status="302")
        return ""
            
    # BlackJaw Members Controller
    @cherrypy.expose('/members')
    def members(self, **args):
        cherrypy.response.headers["Server"] = "PockerServer"
        cookie = cherrypy.response.cookie
        headers = cherrypy.request.headers
        # Check IP Address, proxy chain to allow access to members ressource
        if cherrypy.request.cookie.keys().__contains__("access_cookie") or ("X-Forwarded-For" in headers.keys() and headers["X-Forwarded-For"] in ["localhost", "127.0.0.1"]):
            cookie["access_cookie"] = "0fd4c1a5c6827a12"
            cookie['access_cookie']['path'] = '/'
            cookie['access_cookie']['max-age'] = time.time()+3600
            if cherrypy.request.method == "GET":
                cookie_keys = cherrypy.request.cookie.keys()
                # unserialize cookies if the conditions are met
                if cookie_keys.__contains__("auth") and cookie_keys.__contains__("sh1signature"):
                    auth_cookie = (str(cherrypy.request.cookie["auth"])[17:]).replace('"',"")
                    decoded_auth = ""
                    try:
                        decoded_auth = zlib.decompress(base64.b64decode(auth_cookie))
                        print decoded_auth
                    except:
                        pass
                    result = ObjectDeserialize(decoded_auth)
                    if(checkSignature(auth_cookie,str(cherrypy.request.cookie["sh1signature"]).partition("=")[2])):
                        return MEMBERS_PAGE+"<center><br><br><b> DEBUG : "+str(result)+"<b>"
                    else:
                        return MEMBERS_PAGE+AUTH_ERROR
                else:
                    return MEMBERS_PAGE
            if cherrypy.request.method == "POST":
                username = ""
                code =""
                password=""
                try:
                    username = cherrypy.request.params.get("username",None)
                    code = cherrypy.request.params.get("code",None)
                    password = cherrypy.request.params.get("password",None)
                except:
                    pass
                if headers["Content-Length"]:
                    if username and password and code:
                        # auth and signature cookies factory
                        new_member = uc.Member(username, code, password)
                        access_cookie = base64.b64encode(zlib.compress(ObjectSerialize(new_member)))
                        print access_cookie
                        self.SetCookies(cookie, access_cookie)
                        # On success redirect user to members and display members info
                        cherrypy.response.status = 302
                        cherrypy.response.headers["Location"] = "/members"
                        cherrypy.response.headers["X-Forwarded-For"] = "127.0.0.1"
                        return ""
                    else:
                        return MEMBERS_PAGE+INPUT_ERROR
        elif "access_cookie" not in cookie.keys():
            return error_page_403()
    
    def SetCookies(self, cookie_handle, access_cookie):
        cookie_handle["auth"] = access_cookie
        cookie_handle["auth"]["expires"] = 3600
        cookie_handle['sh1signature'] = hashlib.sha1(access_cookie).hexdigest()
        cookie_handle['sh1signature']['expires'] = 3600
            
# Starting server
cherrypy.config.update({
            'server.socket_host': "0.0.0.0",
            'server.socket_port': 8180,
            'error_page.404': error_page_404,
            'error_page.403': error_page_403,
            'log.error_file' : "error.log",
            'log.screen' : True,
            'tools.sessions.on': True,
            'tools.secureheaders.on':True
})


# Setup server configuration
conf = {
       '/index': {
            'tools.staticdir.on': True,
            'tools.staticdir.root': DIR,
            'tools.staticdir.dir': STATIC_DIR,
            'tools.staticdir.index' : "index.html",
            # 'request.dispatch': dispatcher
        },
        '/.git': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(DIR, '.git'),
            'tools.gzip.on': True,
            'tools.staticdir.debug': True,
            'tools.staticdir.index' : "git.zip",
        },
        '/favicon.png': {
            'tools.staticdir.on': True,
            'tools.staticdir.root': DIR,
            'tools.staticdir.dir': os.path.join(STATIC_DIR, 'favicon.png'),
        }

}

cherrypy.quickstart(WebServer(), "/", config=conf)
cherrypy.engine.start()

