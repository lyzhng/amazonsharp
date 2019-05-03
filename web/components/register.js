import Vue from 'vue';
import Vuetify from 'vuetify';
import Register from 'Register/Register.vue';

import 'vuetify/dist/vuetify.min.css';

const rootElement = document.getElementsByTagName('app')[0];
const rootComponent = Vue.extend(Register);

Vue.use(Vuetify);
new rootComponent({
    el: 'app',
    render: h => h(Register, {
        props: { ...rootElement.dataset },
    }),
});
