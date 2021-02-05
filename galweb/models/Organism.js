const Sequelize = require('sequelize');
const db = require('../config/database');

const Organism = db.define('Organism', {
    ID:{
        type: Sequelize.INTEGER(11),
        allowNull: false,
        autoIncrement: true,
        primaryKey: true
    }, 
    TAXON_ID: {
      type: Sequelize.INTEGER
    },
    SPECIES: {
      type: Sequelize.STRING
    },
    STRAIN: {
      type: Sequelize.STRING
    },
    PHYLUM: {
      type: Sequelize.STRING
    },
    FAMILY: {
      type: Sequelize.STRING
    },
    GENUS: {
      type: Sequelize.STRING
    },
    ORDERS: {
      type: Sequelize.STRING
    },
    CLASS: {
      type: Sequelize.STRING
    },
    SUPERKINGDOM: {
      type: Sequelize.STRING
    },
    VERSION: {
      type: Sequelize.FLOAT
    },
    NEW_VERSION: {
        type: Sequelize.FLOAT
      },
    COMMENT: {
        type: Sequelize.FLOAT
      }
    },
    {
        tableName: 'Organism'
    }
    );

module.exports = Organism;
