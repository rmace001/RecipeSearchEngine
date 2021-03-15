var express = require("express");
const bodyParser = require('body-parser');
var path = require('path');
var app = express();

const cassandra = require('cassandra-driver');
const client = new cassandra.Client({ 
    contactPoints: ['127.0.0.1'], 
    localDataCenter: 'datacenter1',  
    keyspace: 'recipes' 
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extend: true}));

app.set('views', './views');
app.set('view engine','ejs');

app.use(express.static('public'));

// Results
var pages = [];

app.get("/",function(req,res){
    res.render("index",{ pages:pages });
});


app.post("/search",function(req,res){
    //testing output
    console.log(req.body.query);
    var str = req.body.query;

    const select = 'SELECT links FROM recipetable WHERE key = ?';
    const params = [ str ] ;
    var data;
    client.execute(select, params, function (err, result) {
        if (err) throw err
        // console.log(result.rows[0]);
        data = result.rows[0].links;
        res.render("index",{ pages:data });
    });

});

const port = 3000;

app.listen(3000, function(){
    console.log("server is on port 3000");
});