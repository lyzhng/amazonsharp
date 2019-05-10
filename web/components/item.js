import Vue from 'vue';
import Vuetify from 'vuetify';
import Item from 'Item/Item.vue';

import 'vuetify/dist/vuetify.min.css';

const rootElement = document.getElementsByTagName('app')[0];
const rootComponent = Vue.extend(Item);

Vue.use(Vuetify);
new rootComponent({
    el: rootElement,
    render: h => h(Item, {
        props: { ...rootElement.dataset },
    }),
});

