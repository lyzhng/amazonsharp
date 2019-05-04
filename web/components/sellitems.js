import Vue from 'vue';
import Vuetify from 'vuetify';
import SellItems from 'SellItems/SellItems.vue';

import 'vuetify/dist/vuetify.min.css';

const rootElement = document.getElementsByTagName('app')[0];
const rootComponent = Vue.extend(SellItems);

Vue.use(Vuetify);
new rootComponent({
    el: rootElement,
    render: h => h(SellItems, {
        props: { ...rootElement.dataset },
    }),
});
