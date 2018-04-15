//Developed by Yrneh for the WPPD Mutual Fund Securities Trading Bot
var fs = require('fs');
var fileData = '';

var analyze = require('Sentimental').analyze,
    positivity = require('Sentimental').positivity,
    negativity = require('Sentimental').negativity;

function analysis(text) {
    result = analyze(text);
    return result;
}

new Promise((resolve, reject) => {
fs.readFile('dataText.txt', (err, data) => {
    fileData = data.toString('utf-8');
    resolve();
});
}).then(() => {
    console.log(analysis(fileData));
});