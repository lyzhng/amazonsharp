<template>
<div>
	<div class="mb-3">
		<v-alert v-if="this.message !== ''"
			value=true
			:type="`${this.messageType}`"
        	outline=true
	    	>
			{{ formattedMessage() }}
		</v-alert>
	</div>
	<v-form method="post">
    	<v-text-field
    		v-model="username"
	    	prepend-icon="account_circle"
    		label="Email Address"
			name="username"
    		required
    		autofocus
    		></v-text-field>
		<v-text-field
    		v-model="password"
    		:append-icon="showPassword ? 'visibility_off' : 'visibility'"
    		:type="showPassword ? 'text' : 'password'"
    		prepend-icon="lock"
    		label="Password"
			name="password"
    		required
    		@click:append="showPassword = !showPassword"
    		></v-text-field>
 	 
		<v-layout row>
    		<v-btn flat small color="info" href="/register">Create Account</v-btn>
    		<v-spacer></v-spacer>
    		<v-btn type="submit" color="info">Login</v-btn>
  		</v-layout>
	</v-form>
</div>
</template>

<script>
export default {
    name: 'LoginForm',
    components: {},
    data: () => ({
        username: "",
        password: "",
        showPassword: false,
    }),
    methods: {
        formattedMessage() {
            if (this.message !== '') {
                return this.message.replace(/^Error: /, '');
            }
			return this.message;
        },
    },
    props: ['message', 'messageType'],
}
</script>
