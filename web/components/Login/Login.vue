<template>
<v-app id="inspire">
  	<v-content>
    	<v-container fluid fill-height>
      		<v-layout align-center>
        		<v-flex xs12 sm8 offset-sm2 md8 offset-md2 lg4 offset-lg4>
					<v-card>
						<v-container>
          					<p class="headline text-xs-center">
								Sign in to continue to Amazon#
            					<!-- <v-img src="/public/assets/logo.png" max-height=175 alt="Tasky" contain class="mb-5"></v-img> -->
          					</p>
          					<login-form :message="this.message" :message-type="this.messageType"></login-form>
						</v-container>
					</v-card>
        		</v-flex>
      		</v-layout>
    	</v-container>
  	</v-content>

  	<footer-component></footer-component>
</v-app>
</template>

<script>
import LoginForm from 'Login/LoginForm.vue';
import FooterComponent from 'Footer/Footer.vue';

export default {
    name: 'Login',
    components: {LoginForm, FooterComponent},
    data: () => ({
    }),
    methods: {
    },
    props: ['message', 'messageType'],
}
</script>
