
// webpack.config.js
const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  resolve: {
  fallback: {
    "util": false,
    "web-vitals": false,
    "fs": false,
    "path": require.resolve("path-browserify")
  }
  },
  // Add other necessary configurations here
};
