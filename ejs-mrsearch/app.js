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
    // for (i = 0; i < lists.length; i++) {
    //     const select = 'SELECT links FROM recipetable WHERE key = ?';
    //     const params = [ lists[i] ] ;
    //     // var data;
    //     client.execute(select, params, function (err, result) {
    //         if (err) throw err
    //         console.log(result.rows[0]);
    //         console.log(result.rows[0].links);
    //         // var tempe = [];
    //         // tempe = result.rows[0]
    //         // var j = 0;
    //         // for (j = 0; j<tempe.length;j++){
    //         //     console.log(tempe[j])
    //         // }
    //         data_ink.push(result.rows[0].links);
    //         var tempe = [];
    //         tempe = result.rows[0].links
    //         console.log("link list : ",tempe )
    //         // var j = 0;
    //         // for (j = 0; j<tempe.length;j++){
    //         //     console.log("link", j, " is ", tempe[j])
    //         // }
    //         if(data_ink.length == lists.length)
    //             res.render("index",{ pages:data_ink });
    //     });
    // }
    for (i = 0; i < lists.length; i++) {
        const select = 'SELECT * FROM doctable WHERE recipe_link = ?';
        const params = [ lists[i] ] ;
        client.execute(select, params, function (err, result) {
            if (err) 
            return console.error(err);
            data.push(result.rows[0].recipe_title)
            data1.push(result.rows[0].total_time)
            data2.push(result.rows[0].active_time)
            // console.log(data[0])
            if(data.length == lists.length){
                // var pages = JSON.parse('{ recipe_title : data[0], total_time : data[1] ] }');
                // res.render("index", pages );
                res.render("index", { 
                    pages: [data,data1,data2] } );
            }
                
        });
    }
    // console.log(data,data1,data2) can't save the value
});

const port = 3002;

app.listen(port, function(){
    console.log('Express server started on port %s', this.address().port);
});