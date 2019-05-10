<template>
<v-card light height="200px">
	<v-layout row align-center fill-height>
		<v-flex xs4 md3>
			<a :href="itemPath">
				<v-img class="ma-4" :src="imagePath" height="156px"></v-img>
			</a>
		</v-flex>
		<v-flex xs5 md5>
			<v-card-title primary-title>
				<div>
					<div class="headline">{{ name }}</div>
					<div>${{ price }}</div>
                    <div>Quantity: {{ quantity }}</div>
				</div>
			</v-card-title>
		</v-flex>
		<v-flex xs3 md4>
			<v-layout row justify-end class="mr-4">
                <v-dialog v-model="dialog" persistent max-width="600px">
                    <template v-slot:activator="{ on }">
					    <v-icon class="mr-3" v-on="on">edit</v-icon>
                    </template>
                    <new-item-component action="Edit" :name="this.name" :price="this.price"
                                        :image-path="this.imagePath" :quantity="this.quantity"
                                        :seller-email="this.sellerEmail" :item-id="this.itemId"
										@update_vars="updateVars">
                    </new-item-component>
                </v-dialog>
				<v-icon class="ml-3" color="red" @click="$emit('delete_item', itemId)">delete</v-icon>
			</v-layout>
		</v-flex>
	</v-layout>
</v-card>
</template>

<script>
import NewItemComponent from 'SellItems/NewItem.vue';
import FooterComponent from 'Footer/Footer.vue';

export default {
    name: 'SellItemsPreviewComponent',
    components: {FooterComponent, NewItemComponent},
    data: () => ({
		dialog: false,
        drawer: false,
    }),
    methods: {
		updateVars(event) {
			if (event['name'] !== undefined)
				this.name = event['name'];
			if (event['price'] !== undefined)
				this.price = event['price'];
			if (event['quantity'] !== undefined)
				this.quantity = event['quantity'];
			if (event['dialog'] !== undefined)
				this.dialog = event['dialog'];
		},
    },
    props: ['name', 'price', 'imagePath', 'quantity', 'sellerEmail', 'itemId', 'itemPath'],
}
</script>
