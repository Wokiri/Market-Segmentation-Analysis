const path = require("path");
const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const dir_name = 'mkt_analysis_django'

module.exports = {
  entry: {
    mkt_analysis_map: "./src/js/mkt_analysis_map.js",
    ward_detail_map: "./src/js/ward_detail_map.js",
    bootstrap: "./src/js/bootstrap.js",
    market_segmentation: "./src/js/market_segmentation.js",
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

      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },

      {
        test: /\.(woff|woff2|eot|ttf|otf)$/i,
        type: 'asset/resource',
      },
    ],
  },

  plugins: [
    // new webpack.DefinePlugin({
    //   "process.env.NODE_ENV": JSON.stringify(process.env.NODE_ENV),
    //   "process.env.NODE_DEBUG": JSON.stringify(process.env.NODE_DEBUG),
    //   "process.type": JSON.stringify(process.type),
    //   "process.version": JSON.stringify(process.version),
    // }),
    new webpack.DefinePlugin({
      "process.env": {
        NODE_ENV: JSON.stringify("production"),
        // NODE_ENV: JSON.stringify("development"),
      },
    }),
    new MiniCssExtractPlugin({ filename: "[name].css" }),
    new HtmlWebpackPlugin({
      title: dir_name.replace(/_/g, ' ').toUpperCase(),
      template: "./index.html",
    }),
  ],
};
