<template>
<v-app id="inspire" dark>
    <v-navigation-drawer clipped fixed v-model="drawer" app>
        <v-list>
            <v-dialog v-model="dialog" persistent max-width="600px">
                <template v-slot:activator="{ on }">
                    <v-list-tile v-on="on">
                        <v-list-tile-action>
                            <v-icon>add</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Sell Item</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </template>
                <new-item-component action="New" v-model="dialog"></new-item-component>
            </v-dialog>
        </v-list>
    </v-navigation-drawer>

	<v-toolbar app fixed clipped-left>
        <v-toolbar-side-icon class="hidden-md-and-up" @click.stop="drawer = !drawer;"></v-toolbar-side-icon>
		<a href="/">
			<v-toolbar-title>
				<v-img src="/public/assets/logo.png" contain height="38px" width="147px"></v-img>
			</v-toolbar-title>
		</a>

        <v-spacer></v-spacer>
        <v-toolbar-items>
            <v-btn flat href="/logout">
                <v-icon>fa fa-sign-out-alt</v-icon>
                <span class="ml-2">Logout</span>
            </v-btn>
        </v-toolbar-items>
  	</v-toolbar>
  
  	<v-content>
		<v-parallax src="/public/assets/light-3.png" height="100%">
			<v-card class="ma-4" light>
				<div class="display-3 ma-4">Sell Items</div>
					
	 			<v-layout column>
					<v-divider></v-divider>
	  				<v-flex v-for="item in items">
	  					<sell-items-preview-component :name="item.name" :price="item.price" :image-path="item.image-path" :quantity="item.quantity"></sell-items-preview-component>
	  				</v-flex>
	  			</v-layout>
			</v-card>
		</v-parallax>
	</v-content>
  
  	<footer-component></footer-component>
</v-app>
</template>

<script>
import FooterComponent from 'Footer/Footer.vue';
import NewItemComponent from 'SellItems/NewItem.vue';
import SellItemsPreviewComponent from 'SellItems/SellItemsPreview.vue';

export default {
    name: 'SellItems',
    components: {FooterComponent, NewItemComponent, SellItemsPreviewComponent},
    data: () => ({
        dialog: false,
        drawer: true,
		items: [
			{'name': 'Item A', 'price': '$9.99', quantity: 3, 'image-path': 'randomPath'},
			{'name': 'Item B', 'price': '$10.99', quantity: 3, 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', quantity: 3, 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', quantity: 3, 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', quantity: 3, 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', quantity: 3, 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', quantity: 3, 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', quantity: 3, 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', quantity: 3, 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', quantity: 3, 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', quantity: 3, 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', quantity: 3, 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', quantity: 3, 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', quantity: 3, 'image-path': 'randomPath2'},
		],
    }),
    methods: {
		postNewItemForSale() {
			console.log("Seller wants to post new item for sale!");
		},
    },
    props: ['loggedInState'],
}
</script>
