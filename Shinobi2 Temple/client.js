var rpc = require('json-rpc2');

var client = rpc.Client.$create(5000, 'localhost');

// Call add function on the server

client.call('add', [1, 2], function(err, result) {
    console.log('1 + 2 = ' + result);
});