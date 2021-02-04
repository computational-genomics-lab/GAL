const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('mysql', 'root', 'test', {
  host: 'localhost',
  port: 8083,
  dialect: 'mysql'
});

module.exports = sequelize;