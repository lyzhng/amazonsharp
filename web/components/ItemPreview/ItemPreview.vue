<template>
<v-card>
	<v-img src="/public/assets/temp.jpg" contain></v-img>
	<v-card-title primary-title>
		<div>
			<h3 class="headline mb-0">{{ this.name }}</h3>
			<div>{{ this.price }}</div>
		</div>
	</v-card-title>
</v-card>
</template>

<script>
export default {
	name: 'ItemPreviewComponent',
	components: {},
	data: () => ({

	}),
	methods: {

	},
	props: ['name', 'price', 'imagePath'],
}
</script>
