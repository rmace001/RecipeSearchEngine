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
    // console.log(req.body.query);
    var str = req.body.query;
    var lists = str.split(" ");
    console.log(lists)
    var i;
    const data_ink = [];
    const data = [];
    const data1 = [];
    const data2 = [];
    const data3 = [];
    const data4 = [];
    const data_check = [];
    for (i = 0; i < lists.length; i++) {
        const select = 'SELECT links FROM recipetable WHERE key = ?';
        const params = [ lists[i] ] ;
        // var data;
        client.execute(select, params, function (err, result) {
            if (err) throw err
            console.log(result.rows[0]);
            console.log(result.rows[0].links);
            data_ink.push(result.rows[0].links);
            var tempe = [];
            tempe = result.rows[0].links
            var te = tempe.split("'");
            var tecount = 0;
            for (var tecount; tecount < te.length; tecount++ ){
                if (tecount%2 != 0){
                    data.push(te[tecount]) // keep all link of keyword
                }
            }
            if(data_ink.length == lists.length){ // CHECK THE ALL LINK FROM KEY WORD WE GET
                console.log("link is here !!",data);
                var j = 0
                for (j = 0; j < data.length; j++) {
                    const select = 'SELECT * FROM doctable WHERE recipe_link = ?';
                    const params = [ data[j] ] ;
                    client.execute(select, params, function (err1, result1) {
                        if (err1) 
                        return console.error(err1);
                        data_check.push(result1.rows[0])
                        // console.log("check here ", data[j], result1.rows[0] )
                        data1.push(result1.rows[0].recipe_title)
                        data2.push(result1.rows[0].total_time)
                        data3.push(result1.rows[0].active_time)
                        data4.push(result1.rows[0].recipe_link )
                        if( data_check.length ==data.length){
                            console.log("Final",data1, data2,data3,data4)
                            res.render("index", { 
                                pages: [data1,data2,data3,data4] } );
                        }
                            
                    });
                }
            }
            
        });
    }
});

const port = 3002;

app.listen(port, function(){
    console.log('Express server started on port %s', this.address().port);
});