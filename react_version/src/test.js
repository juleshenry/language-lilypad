const { Sequelize, DataTypes } = require('sequelize');
const path = require('path');

const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: path.join(__dirname, 'palabras.db')
});

(async () => {
  try {
    await sequelize.authenticate();
    console.log('Connection has been established successfully.');

    // Your database operations go here

  } catch (error) {
    console.error('Unable to connect to the database:', error);
  } finally {
    await sequelize.close(); // Close the connection when done
  }
})();

// const Palabra = sequelize.define('Palabra', {
//   palabra: {
//     type: DataTypes.STRING,
//     allowNull: false
//   },
//   word: {
//     type: DataTypes.STRING,
//     allowNull: false
//   }
// }, {
//   tableName: 'palabras',
//   timestamps: false
// });

// (async () => {
//   try {
//     await sequelize.authenticate();
//     console.log('Connection has been established successfully.');

//     const results = await Palabra.findAll({
//       attributes: ['word'],
//       where: {
//         palabra: 'casa'
//       }
//     });

//     console.log('Results:', results);
//   } catch (error) {
//     console.error('Unable to connect to the database:', error);
//   }
// })();