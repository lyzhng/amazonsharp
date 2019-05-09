<template>
<v-app id="inspire" dark>
	<v-toolbar app fixed clipped-left>
    	<v-toolbar-side-icon class="hidden-md-and-up" @click.stop="drawer = !drawer;"></v-toolbar-side-icon>
		<a href="/">
			<v-toolbar-title>
				<v-img src="/public/assets/logo.png" contain height="38px" width="147px"></v-img>
			</v-toolbar-title>
		</a>
		<v-spacer></v-spacer>

		<v-toolbar-items class="hidden-sm-and-down" v-if="loggedInState === 'True'">
			<v-menu offset-y>
				<template v-slot:activator="{ on }">
					<v-btn flat dark v-on="on">
						My Account
						<v-icon class="mb-2" dark right>fas fa-sort-down</v-icon>
					</v-btn>
				</template>
				<v-list>
        			<v-list-tile href="/logout">
          				<v-list-tile-action>
            				<v-icon>fa fa-sign-out-alt</v-icon>
          				</v-list-tile-action>
          				<v-list-tile-content>
            				<v-list-tile-title>Logout</v-list-tile-title>
          				</v-list-tile-content>
        			</v-list-tile>
				</v-list>
			</v-menu>
      		<v-btn flat href="/cart" v-if="isCustomer === 'True'">
        		<v-icon dark>fas fa-shopping-cart</v-icon>
      		</v-btn>
            <v-btn flat href="/sell_items" v-else>
                <v-icon dark>fas fa-store</v-icon>
            </v-btn>
		</v-toolbar-items>

    	<v-toolbar-items class="hidden-sm-and-down" v-else>
      		<v-btn flat href="/register">
        		<v-icon>fa fa-user-plus</v-icon>
        		<span class="ml-2">Register</span>
      		</v-btn>
      
      		<v-btn flat href="/login">
        		<v-icon>fa fa-sign-in-alt</v-icon>
        		<span class="ml-2">Login</span>
     		</v-btn>
    	</v-toolbar-items>
  	</v-toolbar>
  
  	<v-navigation-drawer left fixed mobile-break-point=102400 v-model="drawer" app>
    	<v-list>
      		<v-list-tile href="/">
        		<v-list-tile-content>
          			Amazon#
        		</v-list-tile-content>
      		</v-list-tile>
      
      		<div v-if="loggedInState === 'True'">
				<v-list-tile href="/cart" v-if="isCustomer === 'True'">
					<v-list-tile-action>
						<v-icon>fas fa-shopping-cart</v-icon>
					</v-list-tile-action>
					<v-list-tile-content>
						<v-list-tile-title>Cart</v-list-tile-title>
					</v-list-tile-content>
				</v-list-tile>
				<v-list-tile href="/sell_items" v-else>
					<v-list-tile-action>
						<v-icon>fas fa-store</v-icon>
					</v-list-tile-action>
					<v-list-tile-content>
						<v-list-tile-title>Store</v-list-tile-title>
					</v-list-tile-content>
				</v-list-tile>
        		<v-list-tile href="/logout">
          			<v-list-tile-action>
            			<v-icon>fa fa-sign-out-alt</v-icon>
          			</v-list-tile-action>
          			<v-list-tile-content>
            			<v-list-tile-title>Logout</v-list-tile-title>
          			</v-list-tile-content>
        		</v-list-tile>
      		</div>

      		<div v-else>
        		<v-list-tile href="/register">
          			<v-list-tile-action>
            			<v-icon>fa fa-user-plus</v-icon>
          			</v-list-tile-action>
          			<v-list-tile-content>
            			<v-list-tile-title>Register</v-list-tile-title>
          			</v-list-tile-content>
        		</v-list-tile>
      
        		<v-list-tile href="/login">
          			<v-list-tile-action>
            			<v-icon>fa fa-sign-in-alt</v-icon>
          			</v-list-tile-action>
          			<v-list-tile-content>
            			<v-list-tile-title>Login</v-list-tile-title>
          			</v-list-tile-content>
        		</v-list-tile>
      		</div>
    	</v-list>
  	</v-navigation-drawer>
  
  	<v-content>
		<v-parallax src="/public/assets/light-3.png" height="100%">
	  		<v-container grid-list-lg>
				<v-layout column align-space-between>
					<v-layout class="ma-3 mt-5 pt-5" row justify-start>
						<span class="display-3 black--text">Items</span>
					</v-layout>

	 				<v-layout row wrap align-end>
	  					<v-flex v-for="(item, j) in items" :key="j" xs4 sm3 md2>
	  						<item-preview-component :seller="item[0]" :name="item[2]" :price="item[4]" :popularity="-1" :image-path="'/get_image/' + item[0] + '/' + item[1]"></item-preview-component>
	  					</v-flex>
	  				</v-layout>
				</v-layout>
	  		</v-container>
		</v-parallax>
	</v-content>
  
  	<footer-component></footer-component>
</v-app>
</template>

<script>
import ItemPreviewComponent from 'ItemPreview/ItemPreview.vue';
import FooterComponent from 'Footer/Footer.vue';

export default {
    name: 'SellerItems',
    components: {ItemPreviewComponent, FooterComponent},
    data: () => ({
        drawer: false,
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
		
    },
    props: ['loggedInState', 'username', 'isCustomer'],
}
</script>

