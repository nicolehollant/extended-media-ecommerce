<template>
<div class="onboarding">
  <div class="overflow-scroll h-screen">
  <div class="logo"><img src="@/assets/logo.svg" class="logo__img"></div>
  <div class="login onboarding__form--wrapper" v-if="mode === 'login'" :key="mode">
    <h1 class="onboarding__form--header">Sign In</h1>
    <div class="onboarding__form">
      <FormInput
        class="onboarding__form--input"
        name="email"
        placeholder="email"
        label="email"
        :value="email"
        :error="emailError"
        @input="e => email = e"
      />
      <FormInput 
        class="onboarding__form--input"
        name="password"
        placeholder="password"
        label="password"
        :value="password"
        :error="passwordError"
        @input="e => password = e"
      />
      <p class="font-medium text-orange-700">{{requestError}}</p>
      <button class="onboarding__form--submit" @click="signIn">Sign In!</button>
    </div>
    <div class="onboarding__alternate">
      don't have an account? 
      <button class="onboarding__alternate--switch-mode" @click="changeMode">register</button>
    </div>
  </div>
  
  <div class="login onboarding__form--wrapper" v-if="mode === 'register'" :key="mode">
    <h1 class="onboarding__form--header">Register</h1>
    <div class="onboarding__form">
      <p class="font-semibold mb-1 text-left text-sm capitalize text-gray-700">avatar:</p>
      <div class="avatar__selector" >
        <button class="avatar__selector--avatar" v-for="(current, index) of avatars" :key="current" @click="avatar = index">
          <img 
            :src="publicPath + current" 
            :class="avatar === index ? 'avatar__selector--avatar-active':'avatar__selector--avatar-inactive'"
          >
        </button>
      </div>

      <FormInput
        class="onboarding__form--input"
        name="email"
        placeholder="email"
        label="email"
        :value="email"
        :error="emailError"
        @input="e => email = e"
      />
      <FormInput
        class="onboarding__form--input"
        name="username"
        placeholder="username"
        label="Username"
        :value="username"
        :error="usernameError"
        @input="e => username = e"
      />
      <FormInput 
        class="onboarding__form--input"
        name="password"
        placeholder="password"
        label="password"
        :value="password"
        :error="passwordError"
        @input="e => password = e"
      />
      <p class="font-medium text-orange-700">{{requestError}}</p>
      <button class="onboarding__form--submit" @click="register">Sign Up!</button>
    </div>
    <div class="onboarding__alternate">
      already have an account? 
      <button class="onboarding__alternate--switch-mode" @click="changeMode">sign in</button>
    </div>
  </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import FormInput from '@/components/ui/FormInput'

import { publicPath, backendurl } from '@/conf'

export default {
  components: {
    FormInput,
  },
  data() {
    return {
      mode: 'login',
      username: '',
      usernameError: '',
      password: '',
      passwordError: '',
      email: '',
      emailError: '',
      requestError: '',
      avatar: 0,
      avatars: [
        "/avatars/avatar1.png",
        "/avatars/avatar2.png",
        "/avatars/avatar3.png",
        "/avatars/avatar4.png",
        "/avatars/avatar5.png",
      ],
      publicPath: publicPath, //process.env.BASE_URL
      // publicPath: "/extended-media-ecommerce", //process.env.BASE_URL
    }
  },
  methods: {
    changeMode(){
      if(this.mode === 'login') this.mode = 'register'
      else this.mode = 'login'
      this.passwordError = ""
      this.emailError = ""
      this.usernameError = ""
      this.requestError = ''
    },
    signIn() {
      console.log(this.password, this.email)
      this.requestError = ''
      let error = false;
      if(this.password.length < 5) {
        this.passwordError = "password must be > 5 characters"
        error = true;
      } else { this.passwordError = "" }
      if(!/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(this.email)) {
        this.emailError = "email is invalid"
        error = true;
      } else { this.emailError = "" }
      if (error) return;
      axios.post(backendurl + '/users/login/', {
        email: this.email,
        password: this.password,
      }).then(response => { 
        console.log(response); 
        if(response.status === 200) {
          const data = response.data.data;
          console.log(data)
          this.$store.commit('setUser', { user: data })
          this.$router.push("shop")
        }
      })
      .catch(error => { 
        this.requestError = error.response.data.message || error.response.data || error.response;
        console.log(error.response); 
      });
    },
    register() {
      console.log(this.username, this.password, this.email, this.avatar)
      this.requestError = ''
      let error = false;
      if(this.username.length < 5) {
        this.usernameError = "username must be > 5 characters"
        error = true;
      } else { this.usernameError = "" }
      if(this.password.length < 5) {
        this.passwordError = "password must be > 5 characters"
        error = true;
      } else { this.passwordError = "" }
      if(!/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(this.email)) {
        this.emailError = "email is invalid"
        error = true;
      } else { this.emailError = "" }
      if (error) return;
      const data = {
        username: this.username,
        password: this.password,
        email: this.email,
        avatar: this.avatar,
      }
      axios.post(backendurl + '/users/', data).then(response => { 
        console.log(response); 
        if(response.status === 201) {
          const data2 = response.data.data;
          console.log(data2)
          this.$store.commit('setUser', { user: data })
          this.$router.push("home")
        }
      })
      .catch(error => { 
        this.requestError = error.response.data.message || error.response.data || error.response;
        console.log(error.response); 
      });
    }
  },
}
</script>

<style lang="postcss" scoped>
.onboarding {
  @apply fixed top-0 left-0 w-screen min-h-screen h-full bg-green-300 z-onboarding;
}
.logo {
  @apply w-full m-auto flex-center mt-12 mb-6;
}
.logo__img {
  max-width: calc(100% - 4rem);
  width: 150px;
}
.onboarding__form--wrapper {
  @apply my-6;
}
.onboarding__form--header {
  @apply capitalize text-green-800 font-normal text-2xl leading-loose my-3;
}
.onboarding__form {
  overflow: scroll;
  @apply mx-6 p-6 bg-green-100 rounded-lg shadow mb-4;
}
.onboarding__form--input {
  @apply mb-4;
}

.onboarding__form--submit {
  @apply relative px-8 py-2 mt-4 border-2 border-green-500 font-semibold rounded-full ease;
}
.onboarding__form--submit:hover {
  @apply bg-green-300;
}
.onboarding__form--submit:focus {
  outline: none;
  @apply bg-teal-200;
}

.onboarding__alternate {
  @apply font-medium;
}
.onboarding__alternate--switch-mode {
  @apply relative font-bold text-blue-700;
}
.onboarding__alternate--switch-mode:focus {
  outline: none;
  @apply underline;
}
.onboarding__alternate--switch-mode:hover::after {
  width: calc(100% + 0.5rem);
}
.onboarding__alternate--switch-mode::after {
  content: "";
  left: -0.25rem;
  height: 2px;
  bottom: -0.125rem;
  @apply absolute block bg-blue-700 w-0 ease;
}

.avatar__selector {
  @apply flex items-center mb-4 w-full py-2 border-2 border-transparent bg-transparent;
}
.avatar__selector--avatar {
  width: calc(100% / 5);
  outline: none;
  @apply relative ease-slow;
}
.avatar__selector--avatar:focus::after {
  content: "";
  left: 12.5%;
  height: 1px;
  bottom: 0rem;
  width: 75%;
  @apply absolute block bg-blue-700 ease shadow;
}
.avatar__selector--avatar-inactive {
  filter: saturate(0.3) opacity(0.5) blur(3px);
  transform: scale(0.7);
}
.avatar__selector--avatar img {
  @apply ease-slow;
}
.avatar__selector--avatar-inactive:hover {
  filter: saturate(0.4) opacity(0.6) blur(2px);
  transform: scale(0.75);
  @apply ease;
}
.avatar__selector--avatar-active {
  filter: saturate(1) opacity(1) blur(0);
  transform: scale(1) translateY(-0.5rem);
}

@media (min-width: 600px) {
  .onboarding__form {
    @apply max-w-xl mx-auto mb-8;
  }
  .onboarding__form--wrapper {
    @apply my-12;
  }
  .logo__img {
    max-width: calc(100% - 2rem);
    width: 250px;
  }
  .onboarding__form--header {
    @apply text-3xl my-4;
  }
}
</style>
