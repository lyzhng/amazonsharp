<template>
<v-app id="inspire" light>
  <v-navigation-drawer clipped fixed v-model="drawer" app>
    <v-list>
      <v-list-tile @click="newTask();">
        <v-list-tile-action>
          <v-icon>add</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>New</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
    <v-divider></v-divider>
	<v-list dense>
      <v-list-tile @click="">
      	<v-list-tile-action>
          <v-icon>fa fa-star</v-icon>
      	</v-list-tile-action>
      	<v-list-tile-content>
          <v-list-tile-title>Today</v-list-tile-title>
      	</v-list-tile-content>
      </v-list-tile>
      
      <v-list-tile @click="">
      	<v-list-tile-action>
          <v-icon>fa fa-calendar-alt</v-icon>
      	</v-list-tile-action>
      	<v-list-tile-content>
          <v-list-tile-title>Upcoming</v-list-tile-title>
      	</v-list-tile-content>
      </v-list-tile>
      
   	  <v-list-tile @click="">
      	<v-list-tile-action>
          <v-icon>fa fa-cloud</v-icon>
      	</v-list-tile-action>
      	<v-list-tile-content>
          <v-list-tile-title>Thought Cloud</v-list-tile-title>
      	</v-list-tile-content>
      </v-list-tile>
      
      <v-list-tile @click="">
        <v-list-tile-action>
          <v-icon>fa fa-calendar-check</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>Done</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
  	</v-list>
  </v-navigation-drawer>
  
  <v-toolbar app fixed clipped-left>
  	<v-toolbar-side-icon class="hidden-md-and-up" @click.stop="drawer = !drawer;"></v-toolbar-side-icon>
  	<v-toolbar-title>Tasky</v-toolbar-title>
    
    <v-spacer></v-spacer>
    
    <v-toolbar-items>
        <v-btn flat href="/auth/logout">
          <v-icon>fa fa-sign-out-alt</v-icon>
          <span class="ml-2">Logout</span>
        </v-btn>
      </v-toolbar-items>
	</v-toolbar>

    <footer-component></footer-component>
  </v-app>
</template>

<script>
import FooterComponent from 'Footer/Footer.vue';

export default {
    name: 'AmazonSharp',
    components: {FooterComponent},
    data: () => ({
        drawer: null,
        tasks: [],
    }),
    methods: {
    },
    props: ['username'],
}
</script>
