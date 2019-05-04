import Vue from 'vue';
import Vuetify from 'vuetify';
import AllItems from 'AllItems/AllItems.vue';

import 'vuetify/dist/vuetify.min.css';

const rootElement = document.getElementsByTagName('app')[0];
const rootComponent = Vue.extend(AllItems);

Vue.use(Vuetify);
new rootComponent({
    el: rootElement,
    render: h => h(AllItems, {
        props: { ...rootElement.dataset },
    }),
});

