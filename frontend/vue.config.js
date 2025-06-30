const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      // Proxy pour l'API Django
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: { '^/api': '/api' },
        logLevel: 'debug',
        secure: false,
        onProxyReq: (proxyReq) => {
          // Ajouter les en-têtes nécessaires pour les requêtes CORS
          proxyReq.setHeader('Origin', 'http://localhost:8081');
          proxyReq.setHeader('Referer', 'http://localhost:8081');
          // Ajouter le header X-Forwarded-Proto pour les requêtes HTTPS
          proxyReq.setHeader('X-Forwarded-Proto', 'http');
        },
        onProxyRes: (proxyRes) => {
          // S'assurer que les en-têtes CORS sont correctement définis dans la réponse
          proxyRes.headers['Access-Control-Allow-Origin'] = 'http://localhost:8081';
          proxyRes.headers['Access-Control-Allow-Credentials'] = 'true';
          proxyRes.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS';
          proxyRes.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization, X-CSRFToken';
        }
      },
      '/blood-bank': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: { '^/blood-bank': '/api/blood-bank' },
        logLevel: 'debug',
        secure: false,
        onProxyReq: (proxyReq) => {
          proxyReq.setHeader('Origin', 'http://localhost:8081');
          proxyReq.setHeader('Referer', 'http://localhost:8081');
          proxyReq.setHeader('X-Forwarded-Proto', 'http');
        },
        onProxyRes: (proxyRes) => {
          proxyRes.headers['Access-Control-Allow-Origin'] = 'http://localhost:8081';
          proxyRes.headers['Access-Control-Allow-Credentials'] = 'true';
          proxyRes.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS';
          proxyRes.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization, X-CSRFToken';
        }
      },
      // Proxy pour Orthanc - Utilisation d'un chemin spécifique pour éviter les conflits
      '/orthanc-api': {
        target: 'http://localhost:8042',
        changeOrigin: true,
        pathRewrite: { '^/orthanc-api': '' }, // Retire '/orthanc-api' de l'URL
        logLevel: 'debug',
        secure: false,
        onProxyReq: (proxyReq) => {
          // Ne pas ajouter d'en-têtes spécifiques ici, laisser le navigateur les gérer
          proxyReq.removeHeader('X-CSRFToken');
          proxyReq.removeHeader('Cookie');
        }
      }
    },
    hot: true,
    client: {
      webSocketURL: 'auto://0.0.0.0:0/ws',
      overlay: {
        errors: true,
        warnings: false,
      },
    },
  },
  chainWebpack: config => {
    config.plugin('html').tap(args => {
      args[0].title = 'MedLink - Plateforme de Télémédecine';
      return args;
    });
  },
  configureWebpack: {
    devtool: 'source-map', // Améliore le débogage
  },
  css: {
    sourceMap: true,
    loaderOptions: {
      sass: {
        additionalData: `@import "@/assets/scss/variables.scss";`
      }
    }
  }
})
