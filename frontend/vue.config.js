const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  chainWebpack: config => {
    config.plugin('html')
      .tap(args => {
        args[0].title = 'Blog Manager';
        args[0].favicon = './public/favicon.ico';
        return args;
      });
  },
  transpileDependencies: [
    'vuetify'
  ]
})
