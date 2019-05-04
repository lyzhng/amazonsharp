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
	<v-form ref="form" method="post">
  		<v-text-field
    		v-model="username"
    		:rules="[rules.emailcheck]"
    		prepend-icon="account_circle"
    		label="Email Address"
			name="username"
    		required
    		autofocus
    		></v-text-field>
		<v-text-field
    		v-model="password"
		    :append-icon="showPassword ? 'visibility_off' : 'visibility'"
		    :rules="[rules.minpassword]"
		    :type="showPassword ? 'text' : 'password'"
		    prepend-icon="lock"
		    label="Password"
			name="password"
		    hint="At least 12 characters"
		    required
		    @click:append="showPassword = !showPassword"
		    ></v-text-field>
		<v-text-field
		    v-model="confirmationPassword"
		    :append-icon="showConfirmationPassword ? 'visibility_off' : 'visibility'"
		    :type="showConfirmationPassword ? 'text' : 'password'"
		    :error-messages="confirmPasswordMatch()"
		    prepend-icon="lock"
		    label="Confirmation Password"
			name="confirm_password"
		    hint="Enter the same password again"
		    required
		    @click:append="showConfirmationPassword = !showConfirmationPassword"
		    ></v-text-field>
        <v-radio-group
            v-model="role"
            :rules="[rules.rolecheck]"
            name="role"
            row>
            <v-radio label="Customer" value="CUSTOMER"></v-radio>
            <v-radio label="Seller" value="SELLER"></v-radio>
        </v-radio-group>

		<v-layout row>
    		<v-btn flat small color="info" href="/login">Sign in instead</v-btn>
    		<v-spacer></v-spacer>
    		<v-btn type="submit" color="info" @click.native="validateForm($event)">Register</v-btn>
  		</v-layout>
	</v-form>
</div>
</template>

<script>
export default {
    name: 'RegisterForm',
    components: {},
    data: () => ({
        username: '',
        password: '',
        confirmationPassword: '',
        showPassword: false,
        showConfirmationPassword: false,
        role: '',
        rules: {
            emailcheck: v => {
                const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                return pattern.test(v) || 'Must be a valid email address';
            },
            rolecheck: v => {
                return v != '' || 'Please select Customer or Seller';
            },
            minpassword: v => v.length >= 12 || 'Needs to be at least 12 characters',
        }
    }),
    methods: {
        formattedMessage() {
            if (this.message !== '') {
                return this.message.replace(/^Error: /, '');
            }
			return this.message;
        },
        confirmPasswordMatch() {
            return (this.password == this.confirmationPassword) ? '' : 'Password does not match';
        },
		validateForm(event) {
			if (this.$refs.form.validate() && this.password == this.confirmationPassword) {
				return true;
			}
			event.stopPropagation();
			event.preventDefault();
		},
    },
    props: ['message', 'messageType'],
}
</script>
