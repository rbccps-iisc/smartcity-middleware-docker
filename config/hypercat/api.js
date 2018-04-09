/** Copyright (c) 2013 Toby Jaffey <toby@1248.io>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

var express = require('express'),
    config = require('./config'),
    path = require('path'),
    http = require('http'),
    fs = require('fs'),
    https = require('https'),
    mongo = require('./mongo'),
    cat = require('./cat'),
    auth = require('./auth');

var app = express();

app.configure(function () {
    app.set('port', config.port);
    // app.use(express.static(__dirname + '/../public'));
    app.use(express.logger('dev'));
    app.use(express.bodyParser());

});

// Routes
// app.get('/', function(req, res) {
//   res.sendfile('./public/index.html');
// });

app.get('/cat', cat.get);
//app.post('/cat', auth.check, cat.post);
app.post('/cat', cat.post);
//app.put('/cat', auth.check, cat.put);

// app.get('/catGraph', cat.getGraphData);

app.put('/cat', cat.put);
app.delete('/cat', cat.delete);

mongo.get(function(err, db) {
    if (err) {
        console.log("Error mongodb %j", err);
        process.exit(1);
    }
    http.createServer(app).listen(app.get('port'), function () {
        console.log("Express server listening on port " + app.get('port'));
    });
});
