<template>
<v-card light height="200px">
	<v-layout row align-center fill-height>
		<v-flex xs3>
			<v-img src="/public/assets/temp.jpg" height="125px" contain></v-img>
		</v-flex>
		<v-flex xs6>
			<v-card-title primary-title>
				<div>
					<div class="headline">{{ this.name }}</div>
					<div> {{ this.price }}</div>
				</div>
			</v-card-title>
		</v-flex>
		<v-flex xs3>
			<v-text-field class="mr-5" type="number" label="Quantity:" value=1 outline></v-text-field>
		</v-flex>
	</v-layout>
</v-card>
</template>

<script>
export default {
	name: 'CartPreviewComponent',
	components: {},
	data: () => ({

	}),
	methods: {

	},
	props: ['name', 'price', 'imagePath'],
}
</script>
