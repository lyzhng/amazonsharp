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
                <new-item-component action="New" :seller-email="this.username"
					@add_item="addItem"></new-item-component>
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
	  				<v-flex v-for="(item, i) in items" :key="i">
	  					<sell-items-preview-component :seller-email="item[0]" :item-id="item[1]" :name="item[2]"
						:price="item[3]" :image-path="item[0]/item[1]" :quantity="item[4]" @delete_item="deleteItem">
						</sell-items-preview-component>
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
		items: null,
    }),
	async mounted() {
		const response = await fetch(`/get_items/${this.username}`);
        if (response.ok) {
            this.items = await response.json();
        } else {
            alert('There was a problem communicating with the server, please try again later.');
            return
        }

		if (this.items === null) {
            this.items = [];
        }
	},
    methods: {
		addItem(event) {
			if (event['dialog'] !== undefined)
				this.dialog = event['dialog'];
			if (event['itemId'] !== undefined) {
				var self = this;
				event['itemId'].then(async function(itemId) {
					const response = await fetch(`/get_items/${self.username}/${itemId}`);
					var itemAttributes = await response.json();
					self.items.push([self.username, itemId, itemAttributes[0], itemAttributes[1], itemAttributes[2]]);
				});
			}
		},

		deleteItem(itemId) {
			if (itemId !== undefined) {
				var xhr = new XMLHttpRequest();
				xhr.open("POST", `/delete_item/${this.username}/${itemId}`, true);
				xhr.send();

				for(var index in this.items) {
					if (this.items[index] === itemId) {
						break;
					}
				}
				this.items.splice(index, 1);
			}
		}
    },
    props: ['loggedInState', 'username'],
}
</script>
