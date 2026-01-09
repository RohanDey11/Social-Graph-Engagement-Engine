<template>
    <h1>Login</h1>
    <div class="login">
      <input type="text" v-model="username" placeholder="Enter Username">
      <input type="password" v-model="password" placeholder="Enter password">
      <button v-on:click="login">Login</button>
      <p>
        <router-link to="/sign-up">Sign Up</router-link>
      </p>
      <div v-if="error">
        <strong>{{ error }}</strong>
      </div>
    </div>
  </template>
  <script>
  import axios from 'axios'
  export default {
    name: 'Login',
    data() {
      return {
        username: '',
        password: '',
        error: null,
        timerId: null 
      }
    },
    methods: {
      async login() {
        if (!this.username || !this.password) {
          this.error = "Add all fields to proceed"
        } else {
          const data = {
            username: this.username,
            password: this.password
          }
          const formData = new FormData();
          for (const key in data) {
            formData.append(key, data[key])
          }
          const result = await axios.post("http://127.0.0.1:5000/login", formData)
          if (result.status == 200) {
            localStorage.setItem("user-info", JSON.stringify(result.data))
            this.$router.push({ name: 'Home' })
  
            // Start the logout timer
            this.timerId = setTimeout(() => {
              localStorage.removeItem('user-info')
              this.$router.push({ name: 'Login' })
            }, 1200000) // Logout after 20 seconds of inactivity
          }
          console.warn(result)
        }
  
      }
    },
    mounted() {
      let user = localStorage.getItem('user-info');
      if (user) {
        this.$router.push({ name: 'Home' })
  
        // logout timer starting
        this.timerId = setTimeout(() => {
          localStorage.removeItem('user-info')
          this.$router.push({ name: 'Login' })
        }, 1200000)
        // 20minutes
      }
    },
    destroyed() {
      clearTimeout(this.timerId)
    }
  }
</script>
  