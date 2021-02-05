const express = require('express');
const router = express.Router();
const db = require('../config/database');
const Organism = require('../models/Organism');


// router.get('/', (req, res) => { res.send('org')});
router.get('/', (req, res) => 
    Organism.findAll()
    .then(org => {
        console.log(org);
        res.render('index', {
        org})}
        )
    .catch(err => console.log(err)));

module.exports = router;