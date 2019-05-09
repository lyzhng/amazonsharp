import Vue from 'vue';
import Vuetify from 'vuetify';
import Sellers from 'Sellers/Sellers.vue';

import 'vuetify/dist/vuetify.min.css';

const rootElement = document.getElementsByTagName('app')[0];
const rootComponent = Vue.extend(Sellers);

Vue.use(Vuetify);
new rootComponent({
    el: rootElement,
    render: h => h(Sellers, {
        props: { ...rootElement.dataset },
    }),
});


