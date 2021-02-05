const express = require('express');
const path = require('path');
const logger = require('./middleware/logger');
const exphbs = require('express-handlebars');
const bodyParser = require('body-parser');


// Database
const db = require('./config/database');

// Test DB
db.authenticate()
  .then(() => console.log('Database connected...'))
  .catch(err => console.log('Error: ' + err));


const app = express();

// Init middleware
app.use(logger);


// app.get('/', (req, res) => { res.send('index') });

// Body Parser Middleware
//app.use(express.json());
//app.use(express.urlencoded({ extended: false }));

// Handlebars Middleware
app.engine('handlebars', exphbs({defaultlayout: 'main'}));
app.set('view engine', 'handlebars');

// Body Parser
app.use(express.urlencoded({ extended: false }));

/*
// Homepage Route
app.get('/', (req, res) =>
  res.render('index', {
    page: 'index',
  })
);
*/

// Organism page Route
app.use('/', require('./routes/organism'));

// Organism information page Route
app.use('/orginfo', require('./routes/organisminfo'));


// use static path to set the path for the npm modules
app.use('/css', express.static(path.join(__dirname, 'node_modules/bootstrap/dist/css')))
app.use('/js', express.static(path.join(__dirname, 'node_modules/bootstrap/dist/js')))
app.use('/js', express.static(path.join(__dirname, 'node_modules/jquery/dist')))

// animate css
app.use('/css', express.static(path.join(__dirname, 'node_modules/animate.css')))
// for node-waves 
app.use('/css/waves.css', express.static(path.join(__dirname, 'node_modules/node-waves/dist/waves.css')))
app.use('/js/waves.js', express.static(path.join(__dirname, 'node_modules/node-waves/dist/waves.js')))
// <!-- Slimscroll Plugin Js -->
app.use('/js/jquery.slimscroll.js', express.static(path.join(__dirname, 'node_modules/jquery-slimscroll/jquery.slimscroll.js')))

// Set static folder
app.use(express.static(path.join(__dirname, 'public')));


const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server started on port ${PORT}`));
