<template>
<v-card light>
    <v-card-title>
        <span class="display-1">{{ this.action }} Item</span>
    </v-card-title>
    <v-card-text>
        <v-container>
            <v-layout column>
                <v-layout row>
                    <v-text-field label="Name" :value="this.name" required autofocus></v-text-field>
                    <v-spacer></v-spacer>
                    <v-text-field label="Price" :value="this.price" required></v-text-field>
                </v-layout row>
                <v-layout row>
                    <v-text-field type="number" label="Quantity" :value="this.quantity" required></v-text-field>
                </v-layout>
            </v-layout>
        </v-container>
    </v-card-text>
    <v-card-action>
        <v-layout row justify-end>
            <v-btn color="blue darken-1" flat @click="$emit('input', false)">Save</v-btn>
            <v-btn color="blue darken-1" flat @click="$emit('input', false)">Quit</v-btn> 
        </v-layout>
    </v-card-action>
</v-card>
</template>

<script>
export default {
    name: 'NewItemComponent',
    components: {},
    data: () => ({
    }),
    methods: {
    },
    props: ['action', 'name', 'price', 'imagePath', 'quantity', 'dialog'],
}
</script>
