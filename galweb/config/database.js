const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('GAL_cgl_dots', 'root', 'test', {
  host: 'localhost',
  dialect: 'mysql'
});

module.exports = sequelize;