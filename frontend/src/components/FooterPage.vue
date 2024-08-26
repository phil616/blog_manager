
<template>
    <v-footer app>
        <v-row justify="center">
          <v-col class="text-center">
            <p>&copy; {{ new Date().getFullYear() }} Powered by Vue.js, @phil616 All Rights Reserved. <a href="/about"> Learn More</a></p>
          </v-col>
        </v-row>
    </v-footer>
</template>

<script>
export default {
  name: 'FooterPage',
};
</script>

<style scoped>
p{
  color: #000;
  font-size: 14px;
  margin: 0;
}
</style>
