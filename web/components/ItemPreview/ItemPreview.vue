<template>
<v-card dark>
	<v-img :src="this.imagePath" contain></v-img>
	<v-card-title primary-title>
		<div>
			<h3 class="headline mb-0">{{ this.name }}</h3>
			<div>{{ this.price }}</div>
            <div>Popularity: {{ this.popularity }}</div>
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
	props: ['name', 'price', 'popularity', 'imagePath'],
}
</script>
