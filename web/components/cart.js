import Vue from 'vue';
import Vuetify from 'vuetify';
import Cart from 'Cart/Cart.vue';

import 'vuetify/dist/vuetify.min.css';

const rootElement = document.getElementsByTagName('app')[0];
const rootComponent = Vue.extend(Cart);

Vue.use(Vuetify);
new rootComponent({
    el: rootElement,
    render: h => h(Cart, {
        props: { ...rootElement.dataset },
    }),
});
