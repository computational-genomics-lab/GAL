const mysql = require('mysql');


// database: 'database name'
// mysql connection
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'test',
    port: 8083,
  });
  connection.connect((err) => {
    if (err) throw err;
    console.log('Connected!');
  });

  module.exports = connection;
  