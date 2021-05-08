const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const dir_name = 'bootstrap_assets'

module.exports = {
  entry: {
    index: "./src/js/index.js",
    bootstrap: "./src/js/bootstrap.js",
  },

  output: {
    path: path.resolve(__dirname, dir_name),
    filename: "[name].js",
  },

  devServer: {
    port: 2021,
  },

  module: {
    rules: [
      {
        test: /\.css$/i,
        use: [
          MiniCssExtractPlugin.loader, //Extracts css into files
          "css-loader", //Tuns css into common js
        ],
      },

      {
        //transpiles SCSS to js
        test: /\.s[ac]ss$/i,
        use: [
          MiniCssExtractPlugin.loader, //Extract css into files
          "css-loader", //Turns css into common js
          "sass-loader", //Turns scss into css
        ],
      },
    ],
  },

  plugins: [
    new MiniCssExtractPlugin({ filename: "[name].css" }),
    new HtmlWebpackPlugin({
      title: dir_name.replace(/_/g, ' ').toUpperCase(),
      template: "./index.html",
    }),
  ],
};
