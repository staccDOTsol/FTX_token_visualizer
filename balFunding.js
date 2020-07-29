
var tokenPrices = {}
var tokenPriceStarts = {}
var first = true;
const request = require('request')
const express = require('express');
var cors = require('cors');
var app = express();
app.use(cors());
var bodyParser = require('body-parser')
app.use(bodyParser.json()); // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({ // to support URL-encoded bodies
    extended: true
}));
app.set('view engine', 'ejs');
app.listen(process.env.PORT || 8888, function() {});
var theurl = process.env.theurl
          function update(){
request.get('https://ftx.com/api/lt/tokens', function (e, r, d){
	d = JSON.parse(d).result
for (var token in d){
if (d[token].description.indexOf('3X') != -1){	

if (tokenPrices[d[token].name] == undefined){
	tokenPrices[d[token].name] = []
}
tokenPrices[d[token].name].push([new Date().getTime(), d[token].changeBod * 100])
}
}
})
          	
          }
          setInterval(function(){
          	update()
          }, 59 * 1000)
setTimeout(function(){
	update()
}, 1000)
app.get('/update', cors(), (req, res) => {
	tosend = {}
for (name in tokenPrices){
tosend[name] = tokenPrices[name][tokenPrices[name].length-1]
}
    res.json({tokenPrices: tosend})



})

app.get('/', (req, res) => {
	console.log(tokenPrices)
        res.render('indexFunding.ejs', {
            tokenPrices: tokenPrices,
        theurl: theurl
        })

});
