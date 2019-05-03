import Vue from 'vue';
import Vuetify from 'vuetify';
import Login from 'Login/Login.vue';

import 'vuetify/dist/vuetify.min.css';

const rootElement = document.getElementsByTagName('app')[0];
const rootComponent = Vue.extend(Login);

Vue.use(Vuetify);
new rootComponent({
    el: 'app',
    render: h => h(Login, {
        props: { ...rootElement.dataset },
    }),
});
