var fs = require('fs')
var ParseXbrl = require("parse-xbrl")

var files = fs.readdirSync('SEC-Edgar-Data', encoding = 'utf-8');
var filings = null;

var i = 0;

function fillDirectory(ticker){
  var ticker = files[i];
new Promise((resolve)=>{
    try{
    fs.mkdirSync('ParsedData/' + ticker);
    } catch(e){}

    filings = fs.readdirSync('SEC-Edgar-Data/'  + ticker, encoding = 'utf-8');
    resolve();
}).then(() => {
  new Promise((resolve) => {
  for(j in filings){
    writeXBRLFile(j, ticker, resolve);
  }
}).then(()=>{
  i++;
  fillDirectory();
})
});
}

function writeXBRLFile(index, ticker, cb){
    ParseXbrl.parse('SEC-Edgar-Data/' + ticker + '/' + filings[index]).then((data) => {
      console.log('ParsedData/' + ticker + '/' + filings[index].split('.')[0] + '.json');
      fs.writeFileSync('ParsedData/' + ticker + '/' + filings[index].split('.')[0] + '.json', JSON.stringify(data));
      if(index == filings.length -1){
        cb();
      }
    });
}

fillDirectory();
