<template>
<v-app id="inspire" dark>
	<v-toolbar app fixed clipped-right>
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
    
    	<v-toolbar-side-icon class="hidden-md-and-up" @click.stop="drawer = !drawer;"></v-toolbar-side-icon>
  	</v-toolbar>
  
  	<v-navigation-drawer right fixed mobile-break-point=102400 v-model="drawer" app>
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
	  		<v-container grid-list-lg>
				<v-layout column align-space-between>
					<v-carousel hide-delimiters dark>
						<v-carousel-item v-for="(image, i) in images" :key="i">
							<img :src="image.src" style="height:100%;width:100%;" />
						</v-carousel-item>
					</v-carousel>

					<v-layout class="ma-3 mt-5 pt-5" row justify-start>
						<span class="display-3 black--text">Popular Items</span>
					</v-layout>

	 				<v-layout row wrap align-end>
	  					<v-flex v-for="item in items" xs4 sm3 md2>
	  						<item-preview-component :name="item.name" :price="item.price" :image-path="item.image-path"></item-preview-component>
	  					</v-flex>
	  				</v-layout>

					<v-divider></v-divider>
					<v-layout row justify-end>
						<v-btn class="ma-5" dark href="/items">See All</v-btn>
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
    name: 'Index',
    components: {ItemPreviewComponent, FooterComponent},
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
		images: [
			{'src': '/public/assets/carousel-temp1.jpg'},
			{'src': '/public/assets/carousel-temp2.jpg'},
			{'src': '/public/assets/carousel-temp3.jpeg'},
		],
    }),
    methods: {
    },
    props: ['loggedInState'],
}
</script>

