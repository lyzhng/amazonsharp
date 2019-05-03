import Vue from 'vue';
import Vuetify from 'vuetify';
import AmazonSharp from 'AmazonSharp/AmazonSharp.vue';

import 'vuetify/dist/vuetify.min.css';

const rootElement = document.getElementsByTagName('app')[0];
const rootComponent = Vue.extend(Tasky);

Vue.use(Vuetify);
new rootComponent({
    el: 'app',
    render: h => h(Tasky, {
        props: { ...rootElement.dataset },
    }),
});
