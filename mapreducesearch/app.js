// const hostname = 'localhost';
// const port = 3000;
// const server = http.createServer((req, res) => {
//   res.statusCode = 200;
//   res.setHeader('Content-Type', 'text/plain');
//   res.end('Hello World!\n');
// });

// server.listen(port, hostname, () => {
//   console.log(`Server running at http://${hostname}:${port}/`);
// });

const http = require('http')
const fs = require('fs')

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'content-type': 'text/html' })
  fs.createReadStream('index.html').pipe(res)
})

server.listen(process.env.PORT || 3000)




const cassandra = require('cassandra-driver');
const client = new cassandra.Client({ 
    contactPoints: ['127.0.0.1'], 
    localDataCenter: 'datacenter1',  
    keyspace: 'recipes' 
  });

const results = document.getElementById('results');

const searchBar = document.getElementById('searchBar');
let someList = [];

searchBar.addEventListener('keyup', (e) => {
    if (e.code === 'Enter'){
        const searchString = e.target.value;
        console.log(searchString);
        // selectLinks(searchString);
    }
});


function selectLinks(key) {
  
    // TO DO: execute query that retrieves list of links from the table
    console.log(key);

    const select = 'SELECT links FROM recipetable WHERE key = ?';
    const params = [ key ] ;
    return client.execute(select, params, { prepare : true });
}
  
async function main() {
    await client.connect();
    const rs1 = await selectLinks('Pumpkin');
    const links = rs1.first();

    if (links) {
        console.log(links);
    } else {
        console.log("No results");
    }

    await client.shutdown();
}
  
main();