const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('GAL_cgl_dots', 'root', 'test', {
  host: 'localhost',
  port: 8083,
  dialect: 'mysql'
});

module.exports = sequelize;