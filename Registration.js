<<<<<<< HEAD
const express = require('express');
const Datastore = require('nedb');

const app = express();
app.listen(3000, () => console.log('listening at 3000'));
app.use(express.static('public'));
app.use(express.json({ limit: '1mb'}));

const database = new Datastore('database.db');
database.loadDatabase();

=======
function register(phone, pass, pass2)
{
    if(pass != pass2)
    {
        alert("Passwords do not match");
    }
    else
    {
        alert(phone +"\n"+pass+"\n"+pass2);
    }
} 
>>>>>>> parent of 8c2eb86 (no neww)

