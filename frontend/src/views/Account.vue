<template>
<div class="account">
  <div class="account__form--wrapper" v-if="mode === 'default'">
    <h1 class="account__form--header">My Account</h1>
    <div class="message">
      <p class="message-border">Message from the devs:</p>
      <p>
        I'm sorry to say that this is innately missing content. 
        Both paying for and dealing with object storage was, 
        unfortunately, too much work for this assignment 😢
      </p>
      <p class="text-xl font-bold mt-2 text-green-800">💝 Cole</p>
    </div>
    <div class="message">
      <div class="font-medium flex justify-between"><span class="text-left font-semibold capitalize">email:</span> {{user.email}}</div>
      <div class="font-medium flex justify-between"><span class="text-left font-semibold capitalize">username:</span> {{user.username}}</div>
      <div class="font-medium flex justify-between"><span class="text-left font-semibold capitalize">avatar:</span></div>
      <img :src="publicPath + avatar" />
    </div>
    <button class="account__form--submit my-10" @click="changeMode">Update Account</button>
    <div class="account__alternate">
      ready to go? 
      <button class="account__alternate--switch-mode" @click="logout">log out</button>
    </div>
  </div>
  <div class="login account__form--wrapper" v-if="mode === 'update'" :key="mode">
    <h1 class="account__form--header">Update Account</h1>
    <div class="account__form">
      <p class="font-semibold mb-1 text-left text-sm capitalize text-gray-700">new avatar:</p>
      <div class="avatar__selector" >
        <button class="avatar__selector--avatar" v-for="(current, index) of avatars" :key="current" @click="avatarIndex = index">
          <img 
            :src="publicPath + current" 
            :class="avatarIndex === index ? 'avatar__selector--avatar-active':'avatar__selector--avatar-inactive'"
          >
        </button>
      </div>

      <FormInput
        class="account__form--input"
        name="newemail"
        placeholder="new email"
        label="new email"
        :value="email"
        :error="emailError"
        @input="e => email = e"
      />
      <FormInput
        class="account__form--input"
        name="new username"
        placeholder="new username"
        label="new username"
        :value="username"
        :error="usernameError"
        @input="e => username = e"
      />
      <FormInput 
        class="account__form--input"
        name="new password"
        placeholder="new password"
        label="new password"
        :value="password"
        :error="passwordError"
        @input="e => password = e"
      />
      <p class="font-medium text-orange-700">{{requestError}}</p>
      <button class="account__form--submit" @click="updateAccount">Update!</button>
    </div>
    <div class="account__alternate">
      changed your mind? 
      <button class="account__alternate--switch-mode" @click="changeMode">back</button>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import FormInput from '@/components/ui/FormInput'
import { mapGetters } from 'vuex'

import { publicPath, backendurl } from '@/conf'

export default {
  components: {
    FormInput,
  },
  computed: {
    ...mapGetters([
      'user',
      'avatar'
    ])
  },
  data() {
    return {
      mode: 'default',
      username: '',
      usernameError: '',
      password: '',
      passwordError: '',
      email: '',
      emailError: '',
      requestError: '',
      avatarIndex: 1,
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
      if(this.mode === 'default') this.mode = 'update'
      else this.mode = 'default'
      this.passwordError = ""
      this.emailError = ""
      this.usernameError = ""
      this.requestError = ''
    },
    logout(){
      this.$store.commit('setUser', { user: {} })
      this.$cookies.remove('extended-media-user')
      this.$router.push("/")
    },
    updateAccount() {
      console.log(this.username, this.password, this.email, this.avatarIndex)
      this.requestError = ''
      let error = false;
      if(this.username.length < 5 && this.username !== "") {
        this.usernameError = "username must be > 5 characters"
        error = true;
      } else { this.usernameError = "" }
      if(this.password.length < 5 && this.password !== "") {
        this.passwordError = "password must be > 5 characters"
        error = true;
      } else { this.passwordError = "" }
      if(!/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(this.email) && this.email !== "") {
        this.emailError = "email is invalid"
        error = true;
      } else { this.emailError = "" }
      if (error) return;
      const data = {
        "password": this.user.password,
        "email": this.user.email,
        "avatar": this.avatarIndex,
      }
      if(this.username !== "") data["username"] = this.username
      if(this.password !== "") data["new_password"] = this.password
      if(this.email !== "") data["new_email"] = this.email
      axios.put(backendurl + '/users/', data).then(response => { 
        console.log(response); 
        if(response.status === 201) {
          const data2 = response.data.data;
          console.log(data2)
          if(this.username === "") data["username"] = this.user.username
          this.$store.commit('setUser', { user: data })
          setTimeout(() => {
            this.changeMode()
          }, 500);
        }
      })
      .catch(error => { 
        this.requestError = error.response.data.message || error.response.data || error.response;
        console.log(error.response); 
      });
    }
  },
  mounted() {
    this.avatarIndex = this.user.avatar
  }
}
</script>

<style lang="postcss" scoped>
.logo {
  @apply w-full m-auto flex-center mt-12 mb-6;
}
.logo__img {
  max-width: calc(100% - 4rem);
  width: 150px;
}
.account__form--wrapper {
  @apply my-6;
}
.account__form--header {
  @apply capitalize text-green-800 font-semibold text-2xl leading-loose my-3;
}
.account__form {
  overflow: scroll;
  @apply mx-6 p-6 bg-green-100 rounded-lg shadow mb-4;
}
.account__form--input {
  @apply mb-4;
}

.account__form--submit {
  @apply relative px-8 py-2 mt-4 border-2 border-green-500 font-semibold rounded-full ease;
}
.account__form--submit:hover {
  @apply bg-green-300;
}
.account__form--submit:focus {
  outline: none;
  @apply bg-teal-200;
}

.account__alternate {
  @apply font-medium;
}
.account__alternate--switch-mode {
  @apply relative font-bold text-blue-700;
}
.account__alternate--switch-mode:focus {
  outline: none;
  @apply underline;
}
.account__alternate--switch-mode:hover::after {
  width: calc(100% + 0.5rem);
}
.account__alternate--switch-mode::after {
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

.message {
  @apply relative text-lg font-medium mx-6 mt-10 leading-loose p-4 pt-8 border-2 border-green-700 rounded-lg bg-green-100
}
.message-border {
  left: 1rem;
  top: 0;
  transform: translateY(-50%);
  @apply absolute text-xl text-left px-2 py-1 border-2 border-green-700 rounded-lg bg-green-200 leading-tight
}

@media (min-width: 600px) {
  .message {
    @apply max-w-md mx-auto
  }
  .account__form {
    @apply max-w-xl mx-auto mb-8;
  }
  .account__form--wrapper {
    @apply my-12;
  }
  .logo__img {
    max-width: calc(100% - 2rem);
    width: 250px;
  }
  .account__form--header {
    @apply text-3xl my-4;
  }
}
</style>
