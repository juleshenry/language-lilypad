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
let definir = (palabra) => Entry.findOne({
  where : {
    palabra: palabra
  }
}).then(cosa => {
  if (cosa?.definicion) {
    // console.log(cosa.definicion);
    return (cosa.definicion);
  } else {
    console.error('word not found');
    return 0;
  }
}).catch(err => {
  console.error('Error fetching entries:', err);
  return 0;
});

de = definir('locdateli')
de.then((result) => {
  console.log(result); // This will be called when the promise is resolved
}).catch((error) => {
  console.error(error); // This will be called if the promise is rejected
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