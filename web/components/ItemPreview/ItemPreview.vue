<template>
<v-card dark>
	<a :href="this.itemPath">
		<v-img :src="this.imagePath" height="400px" contain></v-img>
	</a>
	<v-card-title primary-title>
		<div>
			<h3 class="headline mb-0">{{ this.name }}</h3>
			<div v-if="seller != undefined">by {{ this.seller }}</div>
			<div>${{ this.price }}</div>
            <div v-if="popularity >= 0">Popularity: {{ this.popularity }}</div>
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
	props: ['name', 'seller', 'price', 'popularity', 'imagePath', 'itemPath'],
}
</script>
