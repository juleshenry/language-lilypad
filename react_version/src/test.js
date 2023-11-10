const { Sequelize, DataTypes } = require('sequelize');
const path = require('path');

const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: path.join(__dirname, 'palabras.db')
});

// Define a model for your entries
const Entry = sequelize.define('palabras', {
  palabra: {
    type: Sequelize.STRING,
    primaryKey: true,
  },
  definicion: Sequelize.TEXT,
},{
  timestamps: false,
}
);


sequelize.sync();

// Query all entries
Entry.findAll({
  where : {
    palabra: "lobo"
  }
}).then(entries => {
  if (entries.length) {
    console.log(entries[0]['dataValues'].definicion);
  } else {
    console.error('word not found');
  }
}).catch(err => {
  console.error('Error fetching entries:', err);
});

// (async () => {
//   try {
//     await sequelize.authenticate();
//     console.log('Connection has been established successfully.');

//     // Your database operations go here

//   } catch (error) {
//     console.error('Unable to connect to the database:', error);
//   } finally {
//     await sequelize.close(); // Close the connection when done
//   }
// })();


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