var rpc = require('json-rpc2');
var http = require('http')
var crypto = require('crypto'),
fs = require('fs')


/* Expose HTTP Server */
http.createServer(function(request, response) {
    fs.readFile('index.html', function(err, data) {
        response.writeHeader(200,
            {'Content-Type': 'text/html',
            'Accept-Ranges': 'bytes',
            'Cache-Control': 'no-cache'    
            });
        response.write(data);
        response.end();
      });
}).listen(8081,'0.0.0.0');

/* JSON-RPC 2.0 Server */
var server = rpc.Server.$create({
    'websocket': true, // is true by default
    'headers': {
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'private, no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache'
    }
});

var file_list = [];


/* md5('meow0851574962') */
var SECRET = "meow0851574962"
var FLAG_FILE = {
    'progress_id' : '7b975a7a0267296ecb9b38e69922486ec267788b',
    'st' : 'active',
    'content' : 'HIC{Dat_JSON_Was_Very_3asyy!!}'
}

generateProgressId = function(filename){
    return crypto.createHash('sha1').update(filename+"::"+SECRET).digest("hex");
}

// console.log(generateProgressId('flag'))

/* Methods Repository */
function add(args, opt, callback) {
    console.log(opt)
  callback(null, args[0] + args[1]);
}

function uploadFile(args, opt, callback){
    resp = ''
    if(!args['filename'] || !args['content']){
        resp = {"error":"Missing parameters filename/content"}
    }else if(!args['progress_id']){
        resp = {"error":"Missing parameter progress_id"}
    }else{
        if(generateProgressId(args['filename']) === args['progress_id']){
            file_list.push(args['content'].toString())
            resp = {"message":"OK"}
        }else{
            resp = {
                "error":"Invalid parameter progress_id",
                "message":"previous action required",
                "data": {
                    "method":"_get_progress_id",
                    "params": ['filename'],
                    "id":"1",
                    "type":"rpc_call"
                    }
                }
        }
    }
    callback(null,resp);
}

/* Mange*/
function getProgressId(args, opt, callback){
  response = ""
  if(args['filename']){
      if(args['filename'] === "flag"){
        response = {"message":"Too baad .. did you think it's that easy ?"}
      }else{
        response = {"progress_id" : generateProgressId(args['filename']),
                "message":"next action required ",
                "data": {
                    "method":"_check_progress_state",
                    "params": ['progress_id'],
                    "id":"3",
                    "type":"notification"
                    }
                
        }
      }
  }else{
    response = {"error":"Missing parameter filename"}
  }
  callback(null, response);
}

// {"jsonrpc": "2.0", "result": {"message":"Check progress notification message", "action":{"method":"_get_file","params":"progrss_id, st","type":"request", "id":4}, "error":"/*SECRET is in rockyou*/ SECRET = 012154545564564 generate_secret: progressID = filename+'::'+SECRET}", "id": "3"}

/* Mange*/
function checkProgressState(args, opt, callback){
    if(args['progress_id']){
          response = {"message":"next action required ",
                  "data": {
                      "method":"_get_file",
                      "params": ['progress_id','st'],
                      "id":"4",
                      "type":"rpc_call"
                      },
                  "error": "Check progress expected notification message, rpc call given .../*SECRET is in rockyou md5(password) */ SECRET = 'f22e7196b9088e56cc3dc831db7f7faf' generate_secret: progressID = sha1(filename+'::'+SECRET)}"
                  }
    }else{
      response = {"error":"Missing parameter filename"}
    }
    callback(null, response);
}


function getFile(args, opt, callback){
    if(args['progress_id']){
        if(args['progress_id'] === "7b975a7a0267296ecb9b38e69922486ec267788b"){
            if(args['st'] === 'active'){
                response = {"message":FLAG_FILE}
            }else{
                response = {"message": "Couldnt get file, error in parameter state",
                        "error": {"st":"inactive"}
                    }
            }
        }else{
          response = {"message": "File service is not available at the moment ..."}
                }
    }else{
      response = {"error":"Missing parameter progress_id or st"}
    }
    callback(null, response);
}


server.expose('add', add);
server.expose('_get_progress_id', getProgressId);
server.expose('_upload_file', uploadFile);
server.expose('_get_file', getFile);
server.expose('_check_progress_state', checkProgressState);


// you can expose an entire object as well:
// server.expose('namespace', {
//     'function1': function(){},
//     'function2': function(){},
//     'function3': function(){}
// });
// expects calls to be namespace.function1, namespace.function2 and namespace.function3

// listen creates an HTTP server on localhost only
server.listen(5200, '0.0.0.0');
console.log("Serving in (0.0.0.0) port 5500")
