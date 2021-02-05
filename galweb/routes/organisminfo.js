const express = require('express');
const router = express.Router();
const db = require('../config/database');
const Organism = require('../models/Organism');
const Sequelize = require('sequelize');
const Op = Sequelize.Op;


router.get('/', (req, res) => {
    
    let taxon_id = parseInt(req.query.taxon);

    Organism.findAll({ where: { TAXON_ID: { [Op.eq]:  taxon_id  } } })
    .then(org => {
        console.log(org);
        res.render('orginfo', {
        org})}
        )
    .catch(err => res.render('error', {error: err}));

});

module.exports = router;

