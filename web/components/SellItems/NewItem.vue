<template>
<v-card light>
    <v-card-title>
        <span class="display-1">{{ this.action }} Item</span>
    </v-card-title>
    <v-card-text>
        <v-container>
            <v-layout column>
                <v-layout row>
                    <v-text-field label="Name" v-model="name" required autofocus></v-text-field>
                    <v-spacer></v-spacer>
                    <v-text-field type="number" step="0.01" label="Price" v-model="price" prefix="$" required></v-text-field>
                </v-layout row>
                <v-layout row>
                    <v-text-field type="number" label="Quantity" v-model="quantity" required></v-text-field>
                </v-layout>
				<v-layout row v-if="this.action == 'New'">
					<v-text-field label="Category" v-model="itemType" required></v-text-field>
				</v-layout>
				<v-layout row>
					<upload-btn class="ma-0 pa-0" title="Upload Image" accept="image/*" @file-update="fileUpload" ></upload-btn>
				</v-layout>
            </v-layout>
        </v-container>
    </v-card-text>
    <v-card-action>
        <v-layout row justify-end>
            <v-btn class="mb-2" color="blue darken-1" flat @click="sendData();">Save</v-btn>
            <v-btn class="mb-2" color="blue darken-1" flat @click="$emit('update_vars', {'dialog': false}); $emit('add_item', {'dialog': false})">Quit</v-btn> 
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
	<v-dialog v-model="this.fileNotUploaded" persistent light max-width="600px">
		<v-card>
			<v-card-title>
				<span class="display-1">Missing Image</span>
			</v-card-title>
			<v-card-text>
				<span>You must upload an image for this listing.</span>
			</v-card-text>
			<v-card-action>
				<v-layout row justify-end>
					<v-btn class="mb-2" color="info" flat @click="removeFileNotUploadedDialog">Ok</v-btn>
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
		imageModified: false,
		imageUploading: false,
		imageUploaded: false,

		fileTypeNotMatch: false,
		fileSizeTooBig: false,
		fileNotUploaded: false,
    }),
    methods: {
		removeFileTypeNotMatchDialog() {
			this.fileTypeNotMatch = false;
		},
		removeFileSizeTooBigDialog() {
			this.fileSizeTooBig = false;
		},
		removeFileNotUploadedDialog() {
			this.fileNotUploaded = false;
		},
		uploadImage(sellerEmail, file) {
			var formData = new FormData();
			formData.append('image', file);

			var uploadURL = `/upload_image/${sellerEmail}/${this.itemId}`;

			var self = this;
			var uploadImageXHR = new XMLHttpRequest();
			uploadImageXHR.open('POST', uploadURL, true);
			uploadImageXHR.send(formData);
			uploadImageXHR.onreadystatechange = function() {
				if (uploadImageXHR.readyState == 4 && uploadImageXHR.status >= 200 && uploadImageXHR.status < 300) {
					self.imageUploaded = true;
				}
			};
		},
		fileUpload(file) {
			this.imageModified = true;
			this.imageUploading = true;

			if (!file.type.match('image.*')) {
				// display type error
				this.fileTypeNotMatch = true;
				return;
			} else if (file.size > 200 * 1024) {
				// display size error
				this.fileSizeTooBig = true;
				return;
			}

			if (this.action === 'New') {
				var self = this;
				var xhr = new XMLHttpRequest();
				xhr.open('POST', `/get_item_id/${this.sellerEmail}`, true);
				xhr.send();
				xhr.onreadystatechange = function() {
					if (xhr.readyState == 4 && xhr.status >= 200 && xhr.status < 300) {
						self.itemId = JSON.parse(xhr.responseText);
						self.uploadImage(self.sellerEmail, file);
					};
				}
			} else if (this.action === 'Edit') {
				this.uploadImage(this.sellerEmail, file);
			}
		},
		sendData() {
			if (this.action === 'New' && !this.imageUploaded) {
				if (!this.imageUploading)
					this.fileNotUploaded = true;
				return;
			}
			
			this.imageUploaded = false;
			this.imageUploading = false;

			var formData = new FormData();
			formData.append('name', this.name);
			formData.append('price', this.price);
			formData.append('quantity', this.quantity);

			var uploadURL;
			if (this.action == 'New') {
				uploadURL = `/add_item/${this.sellerEmail}`;
				formData.append('itemType', this.itemType);
			}
			else if (this.action == 'Edit') {
				uploadURL = `/update_item/${this.sellerEmail}/${this.itemId}`;
			}

			var xhr = new XMLHttpRequest();
			xhr.open('POST', uploadURL, true);
			xhr.send(formData);

			var self = this;
			xhr.onreadystatechange = function() {
				if (xhr.readyState == 4 && xhr.status >= 200 && xhr.status < 300) {
					if (self.action === 'New') {
						self.$emit('add_item', {
							'itemId': self.itemId,
							'sellerEmail': self.sellerEmail, 
							'dialog': false
						});
					} else if (self.action === 'Edit') {
						self.$emit('update_vars', {
							'name': self.name,
							'price': self.price,
							'quantity': self.quantity,
							'dialog': false,
							'imageModified': self.imageModified,
						});
					}
					self.imageModified = false;
				}
			};
		},
    },
    props: ['action', 'name', 'price', 'imagePath', 'itemType', 'quantity', 'sellerEmail', 'itemId'],
}
</script>
