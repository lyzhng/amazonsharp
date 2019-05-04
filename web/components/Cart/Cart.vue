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

		<v-toolbar-items class="hidden-sm-and-down" v-if="loggedInState === 'true'">
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
      		<v-btn flat href="/cart">
        		<v-icon dark>fas fa-shopping-cart</v-icon>
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
      
      		<div v-if="loggedInState === 'true'">
				<v-list-tile href="/cart">
					<v-list-tile-action>
						<v-icon>fas fa-shopping-cart</v-icon>
					</v-list-tile-action>
					<v-list-tile-content>
						<v-list-tile-title>Cart</v-list-tile-title>
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
			<v-card class="ma-4" light>
					<div class="display-4 ma-4">Shopping Cart</div>
					
	 				<v-layout column>
						<v-divider></v-divider>
	  					<v-flex v-for="item in items">
	  						<cart-preview-component :name="item.name" :price="item.price" :image-path="item.image-path"></cart-preview-component>
	  					</v-flex>
	  				</v-layout>

					<v-divider></v-divider>
					<v-layout row justify-end>
						<v-btn class="ma-5" color="info">Place Order</v-btn>
					</v-layout>
			</v-card>
		</v-parallax>
	</v-content>
  
  	<footer-component></footer-component>
</v-app>
</template>

<script>
import FooterComponent from 'Footer/Footer.vue';
import CartPreviewComponent from 'CartPreview/CartPreview.vue';

export default {
    name: 'Cart',
    components: {FooterComponent, CartPreviewComponent},
    data: () => ({
        drawer: false,
		items: [
			{'name': 'Item A', 'price': '$9.99', 'image-path': 'randomPath'},
			{'name': 'Item B', 'price': '$10.99', 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', 'image-path': 'randomPath2'},
			{'name': 'Item B', 'price': '$10.99', 'image-path': 'randomPath2'},
		],
    }),
    methods: {
    },
    props: ['loggedInState'],
}
</script>
