//const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;   // analyze chunk size in dev

module.exports = {
    chainWebpack: (config) => {
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
        },
        progress: false
      },
      configureWebpack: {
        // analyze chunk size
        // plugins: [ new BundleAnalyzerPlugin() ],
        optimization: {},
        watchOptions: {
          ignored: /node_modules/
        },
      }
}