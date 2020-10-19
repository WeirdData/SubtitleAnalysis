import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@fortawesome/fontawesome-free/css/all.css'
import VueWorker from 'vue-worker'

Vue.config.productionTip = false

Vue.use(VueWorker)
new Vue({
    router,
    vuetify,
    render: function (h) {
        return h(App)
    }
}).$mount('#app')
