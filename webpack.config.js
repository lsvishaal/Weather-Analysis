module.exports = {
    entry: './index.html', // Entry point for your application
    output: {
      filename: 'bundle.js', // Output filename for bundled code
      path: path.resolve(__dirname, 'dist'), // Output directory for bundled files
    },
    module: {
      rules: [
        {
          test: /\.js$/, // Rule for JavaScript files
          use: {
            loader: 'babel-loader', // Use Babel loader for transpilation (optional)
            options: {
              presets: ['@babel/preset-env'], // Babel presets for browser compatibility
            },
          },
        },
        {
          test: /\.css$/, // Rule for CSS files (optional)
          use: ['style-loader', 'css-loader'], // Loaders for processing CSS
        },
      ],
    },
  };
  