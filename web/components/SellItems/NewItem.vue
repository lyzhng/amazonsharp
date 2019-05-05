<template>
<v-card light>
    <v-card-title>
        <span class="display-1">{{ this.action }} Item</span>
    </v-card-title>
    <v-card-text>
        <v-container>
            <v-layout column>
                <v-layout row>
                    <v-text-field label="Name" :value="this.name" required autofocus></v-text-field>
                    <v-spacer></v-spacer>
                    <v-text-field label="Price" :value="this.price" required></v-text-field>
                </v-layout row>
                <v-layout row>
                    <v-text-field type="number" label="Quantity" :value="this.quantity" required></v-text-field>
                </v-layout>
				<v-layout row>
					<upload-btn class="ma-0 pa-0" title="Upload Image" accept="image/*" :fileChangedCallback="fileUpload"></upload-btn>
				</v-layout>
            </v-layout>
        </v-container>
    </v-card-text>
    <v-card-action>
        <v-layout row justify-end>
            <v-btn class="mb-2" color="blue darken-1" flat @click="$emit('input', false)">Save</v-btn>
            <v-btn class="mb-2" color="blue darken-1" flat @click="$emit('input', false)">Quit</v-btn> 
        </v-layout>
    </v-card-action>
	<v-dialog v-model="this.fileTypeNotMatch" persistent light max-width="600px">
		<v-card>
			<v-card-title>
				<span class="display-1">Bad File Type</span>
			</v-card-title>
			<v-card-text>
				<span>The uploaded file must be an image type.</span>
			</v-card-text>
			<v-card-action>
				<v-layout row justify-end>
					<v-btn class="mb-2" color="info" flat @click="removeFileTypeNotMatchDialog">Ok</v-btn>
				</v-layout>
			</v-card-action>
		</v-card>
	</v-dialog>
	<v-dialog v-model="this.fileSizeTooBig" persistent light max-width="600px">
		<v-card>
			<v-card-title>
				<span class="display-1">Bad File Size</span>
			</v-card-title>
			<v-card-text>
				<span>The uploaded file must be less than 200KB.</span>
			</v-card-text>
			<v-card-action>
				<v-layout row justify-end>
					<v-btn class="mb-2" color="info" flat @click="removeFileSizeTooBigDialog">Ok</v-btn>
				</v-layout>
			</v-card-action>
		</v-card>
	</v-dialog>
</v-card>
</template>

<script>
import UploadButton from 'vuetify-upload-button';

export default {
    name: 'NewItemComponent',
    components: {'upload-btn': UploadButton},
    data: () => ({
		fileUploaded: false,
		fileTypeNotMatch: false,
		fileSizeTooBig: false,
    }),
    methods: {
		removeFileTypeNotMatchDialog() {
			this.fileTypeNotMatch = false;
		},
		removeFileSizeTooBigDialog() {
			this.fileSizeTooBig = false;
		},
		fileUpload(file) {
			if (!file.type.match('image.*')) {
				// display type error
				this.fileTypeNotMatch = true;
				console.log(this.fileTypeNotMatch);
				return;
			} else if (file.size > 200 * 1024) {
				// display size error
				this.fileSizeTooBig = true;
				return;
			}

			var formData = new FormData();
			formData.append('image', file);

			// var uploadURL = `/upload_image/${this.seller_email}/${item_id}`;
			var uploadURL = '/upload_image/testing/123';

			var xhr = new XMLHttpRequest();
			xhr.open("POST", uploadURL, true);
			xhr.send(formData);
			this.fileUploaded = true;
		}
    },
    props: ['action', 'name', 'price', 'imagePath', 'quantity', 'dialog'],
}
</script>
