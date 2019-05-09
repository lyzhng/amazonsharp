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
	<v-stepper v-model="step" vertical>
		<v-stepper-step :complete="step > 1" step="1">Enter username and passwords</v-stepper-step>
		<v-stepper-content step="1">
			<v-form ref="stepOne">
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
				
				<v-layout row>
					<v-btn flat small color="info" href="/login">Sign in instead</v-btn>
					<v-spacer></v-spacer>
					<v-btn color="info" @click="validateStepOne() && (step = 2);">Continue</v-btn>
				</v-layout>
			</v-form>
		</v-stepper-content>

		<v-stepper-step :complete="step > 2" step="2">Configure profile</v-stepper-step>
		<v-stepper-content step="2">
			<v-form ref="stepTwo">
				<v-text-field
					v-model="address"
					prepend-icon="home"
					label="Address"
					name="address"
					hint="Enter your address"
					required
					></v-text-field>
				<v-text-field
					v-model="phoneNumber"
					:error-messages="checkIfDigitsOnly()"
					prepend-icon="contact_phone"
					label="Phone Number"
					name="phone_number"
					hint="Enter your phone number, digits only."
					required
					></v-text-field>

				<v-radio-group
					v-model="role"
					:rules="[rules.rolecheck]"
					name="role"
					row>
					<v-radio label="Customer" value="CUSTOMER"></v-radio>
					<v-radio label="Seller" value="SELLER"></v-radio>
				</v-radio-group>

				<v-layout row justify-end>
					<v-btn color="info" @click="validateStepTwo() && sendData();">Register</v-btn>
				</v-layout>
				</v-form>
		</v-stepper-content>
	</v-stepper>
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
		address: '',
		phoneNumber: '',
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
        },
		step: 1,
		formData: new FormData(),
    }),
    methods: {
        formattedMessage() {
            if (this.message !== '') {
                return this.message.replace(/^Error: /, '');
            }
			return this.message;
        },
		checkIfDigitsOnly() {
			if (this.phoneNumber === '')
				return '';
			if (!this.phoneNumber.match('[0-9]+'))
				return 'The phone number can only contain digits';
			if (this.phoneNumber.length != 10)
				return 'The phone number has to have 10 digits';
			return '';
		},
        confirmPasswordMatch() {
            return (this.password == this.confirmationPassword) ? '' : 'Password does not match';
        },
		validateStepOne() {
			if (this.$refs.stepOne.validate() && this.password == this.confirmationPassword) {
				this.formData.append('username', this.username);
				this.formData.append('password', this.password);
				return true;	
			}
			return false;
		},
		validateStepTwo(event) {
			if (this.$refs.stepTwo.validate()) {
				this.formData.append('address', this.address);
				this.formData.append('phone_number', this.phoneNumber);
				this.formData.append('role', this.role);
				return true;
			}
			return false;
		},
		sendData() {
			var xhr = new XMLHttpRequest();
			xhr.open('POST', '/register', true);
			xhr.send(this.formData);
			xhr.onreadystatechange = function () {
				if (xhr.readyState == 4 && xhr.status == 200) {
					document.open();
					document.write(xhr.responseText);
				}
			}
		},
    },
    props: ['message', 'messageType'],
}
</script>
