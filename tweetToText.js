//Developed by Yrneh for the WPPD Mutual Fund Securities Trading Bot
function getObjects(obj, key, val) {

    var objects = [];

    for (var i in obj) {

        if (!obj.hasOwnProperty(i)) continue;

        if (typeof obj[i] == 'object') {

            objects = objects.concat(getObjects(obj[i], key, val));

        } else

        if (i == key && obj[i] == val || i == key && val == '') { //

            objects.push(obj);

        } else if (obj[i] == val && key == ''){

            if (objects.lastIndexOf(obj) == -1){

                objects.push(obj);

            }

        }

    }

    return objects;

}

function getValues(obj, key) {

    var objects = [];

    for (var i in obj) {

        if (!obj.hasOwnProperty(i)) continue;

        if (typeof obj[i] == 'object') {

            objects = objects.concat(getValues(obj[i], key));

        } else if (i == key) {

            objects.push(obj[i]);

        }

    }

    return objects;

}


var js = require('C:/Users/Henry/Desktop/T.S.A/data.json');

console.log(getValues(js,'text'));

var fs = require('fs');

fs.writeFile('dataText.txt', getValues(js,'text'), function(err){
    if(err){
        return console.log(err)
    }
    console.log('File created!');
});