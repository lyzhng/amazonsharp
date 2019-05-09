import Vue from 'vue';
import Vuetify from 'vuetify';
import SellerItems from 'SellerItems/SellerItems.vue';

import 'vuetify/dist/vuetify.min.css';

const rootElement = document.getElementsByTagName('app')[0];
const rootComponent = Vue.extend(SellerItems);

Vue.use(Vuetify);
new rootComponent({
    el: rootElement,
    render: h => h(SellerItems, {
        props: { ...rootElement.dataset },
    }),
});

