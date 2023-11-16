const {
  Sequelize,
  DataTypes
} = require('sequelize');
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
}, {
  timestamps: false,
});

sequelize.sync();

// Query all entries
async function definir(palabra) {
  try {
    const entries = await Entry.findOne({
        where: {
            palabra: palabra
        }
    });
    return entries;
  } catch (error) {
    throw new Error('Error fetching entries');
  }
}

async function ass(pa) {
  try {
      const result1 = await definir(pa);
      const result2 = await definir('locomóvil');
      // const a = await result2.definicion.split(" ").map(word => 
      //   definir(word).then(finalResult => {
      //     // Use the final result here
      //     return finalResult
      //   })
      //   .catch(error => {
      //     return (error);
      //   })  
      // );
      return result2;
  } catch (error) {
      // Handle any errors that might occur in the chain
      console.error(error);
  }
}

// ass('loción').then(finalResult => {
//   // Use the final result here
//   console.log(finalResult.definicion)
// })
// .catch(error => {
//   // Handle any errors from the main async function
//   console.error(error);
// });


// async function lilypad(palabra) {
//     result.definicion.split(" ").forEach(element => {
//       console.log('$$$', element);
//       x = definir(element);
//       x.then((rr) => {
//         return rr?.definicion;
//       });
//       // console.log('@',x);
//     });
//     return result.definicion;
//   }).catch((error) => {
//     console.error(error); 
//     // return "";
//   });
// }
// ll = lilypad('loción');
// console.log(lilypad)

// definir('loción')
//     .then(finalResult => {
//         // Use the final result here
//         console.log(finalResult.definicion)
//     })
//     .catch(error => {
//         // Handle any errors from the main async function
//         console.error(error);
//     });
// Map an async function to the array of strings
async function mapDefinirToWords(array) {
  try {
      const promises = array.map(str => definir(str));
      const results = await Promise.all(promises);
      return results;
  } catch (error) {
      throw new Error('Error mapping async function to strings');
  }
}

const defy = "Se dice especialmente de las máquinas de vapor que, por estar montadas sobre ruedas a propósito, pueden trasladarse a donde sean necesarias. U. t. c. s. f."

// Call the function
mapDefinirToWords(defy.split(' '))
  .then(result => {
      result.forEach((x)=> {
        console.log(x?.dataValues?.palabra, x?.dataValues?.definicion?.slice(0,27));
      });
  })
  .catch(error => {
      console.error(error); // Handle any errors that might occur
  });
module.exports = definir;