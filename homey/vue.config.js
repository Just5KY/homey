const { defineConfig } = require('@vue/cli-service');
const CompressionPlugin = require("compression-webpack-plugin");
const ThreeMinifierPlugin = require("@yushijinhun/three-minifier-webpack");
const threeMinifier = new ThreeMinifierPlugin();

//const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: (config) => { 
    config.plugins.delete('prefetch');
    config.module
      .rule("yaml")
      .test(/\.ya?ml$/)
      .use("raw-loader")
      .loader("raw-loader")
      .end();
  },
  // development API proxy
  devServer: {
    proxy: {
      "^/api/": {
        target: "http://localhost:9101",
        secure: false,
        pathRewrite: {
          '/api/*': '/'
        }
      }
    }
  },
  configureWebpack: {
    plugins: [
      new CompressionPlugin({ threshold: 5120 }),
      threeMinifier
    ],
    resolve: {
      plugins: [
        threeMinifier.resolver
      ]
    },
    watchOptions: {
      ignored: /node_modules/
    },
  },
})

