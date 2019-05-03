import Vue from 'vue';
import Vuetify from 'vuetify';
import Index from 'Index/Index.vue';

import 'vuetify/dist/vuetify.min.css';

const rootElement = document.getElementsByTagName('app')[0];
const rootComponent = Vue.extend(Index);

Vue.use(Vuetify);
new rootComponent({
    el: rootElement,
    render: h => h(Index, {
        props: { ...rootElement.dataset },
    }),
});
