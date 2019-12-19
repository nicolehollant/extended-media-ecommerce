<template>
<div class="orders">
  <h1>Orders</h1>

  <div class="login" v-if="!loggedIn">
    <FormInput
        class="onboarding__form--input"
        name="adminUsername"
        placeholder="adminUsername"
        label="adminUsername"
        :value="adminUsername"
        @input="e => adminUsername = e"
      />
    <FormInput
        class="onboarding__form--input"
        name="adminPassword"
        placeholder="adminPassword"
        label="adminPassword"
        :value="adminPassword"
        @input="e => adminPassword = e"
      />
      <button class="admin__login-button--submit" @click="loadOrders">View Orders</button>
  </div>


  <div class="order__list" v-else>
    <table>
      <tr class="table-row__header">
        <td>Email:</td>
        <td>Time:</td>
        <td>Items:</td>
      </tr>
      <tr v-for="order in orders" :key="order.order + 'email'" class="table-row">
        <td>{{ order.email }}</td>
        <td>{{ order.order.split('___')[1] }}</td>
        <td>
            {{ order.items.join(', ') }}
        </td>
      </tr>
    </table>
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
      error: '',
      success: false,
      orders: null,
      adminPassword: '',
      adminUsername: '',
      loggedIn: false,
      publicPath: publicPath, //process.env.BASE_URL
      // publicPath: "/extended-media-ecommerce", //process.env.BASE_URL
    }
  },
  methods: {
    remove(item) {
      this.$store.commit('removeItem', {item: item})
    },
    loadOrders() {
      const data = {
        password: this.adminPassword,
        username: this.adminUsername,
      }
      axios.post(backendurl + '/orders/all/', data).then(response => { 
        console.log(response); 
        if(response.status === 200) {
          this.error = ''
          this.loggedIn = true
          this.success = true
          this.orders = response.data.data;
        }
      })
      .catch(error => { 
        this.error = error;
        console.log(error); 
      });
    }
  },
}
</script>

<style scoped lang="postcss">
.orders {
  margin: auto;
}
.order__item {
  @apply text-lg font-medium my-1;
}
.admin__login-button--submit {
  @apply relative px-8 py-2 mt-4 mb-4 border-2 border-green-500 font-semibold rounded-full ease;
}
.admin__login-button--submit:hover {
  @apply bg-green-300;
}
.admin__login-button--submit:focus {
  outline: none;
  @apply bg-teal-200;
}
.login {
  @apply max-w-lg mx-auto p-4 border-2 border-green-700 rounded-lg bg-green-100;
}
.onboarding__form--input {
  @apply mb-4;
}
.table-row__header td {
  @apply bg-green-900
}
.table-row__header {
  @apply font-semibold text-xl text-green-200;
}
.table-row {
  @apply font-medium text-lg;
}
td {
  @apply px-4 py-2
}

h1 {
  @apply text-3xl font-semibold my-8;
}
table {
  max-width: calc(100vw - 6rem);
  @apply relative mx-auto rounded shadow-xl
}
.table-wrapper {
  width: max-content;
  @apply bg-gray-200 p-4 m-auto;
}
tr:nth-child(even) {
  @apply bg-gray-200 p-2;
}
tr:nth-child(odd) {
  @apply bg-gray-100 p-2;
}
.preview {
  @apply w-20 h-20 mr-2 rounded p-2;
}
.name, .date {
  @apply font-semibold mx-2;
}
.name {
  @apply capitalize text-left;
}
.date {
  @apply text-right;
}
.remove {
  left: calc(100% + 1.5rem);
  height: 5rem;
  @apply absolute font-black text-2xl;
}
.submit {
  @apply relative px-4 py-2 border-2 border-green-500 font-semibold rounded-full ease mt-8;
}
.submit:hover {
  @apply bg-green-300;
}
.submit:focus {
  outline: none;
}
@media (min-width: 600px) {
.preview {
  @apply w-20 h-20 mr-12 rounded p-2;
}
.name, .date {
  @apply font-semibold mx-12;
}
}

@media (min-width: 920px) {
table {
  max-width: 800px;
  position: relative;
}
.remove {
  left: calc(100% + 3rem);
  height: 5rem;
  @apply absolute font-black text-2xl;
}
}
</style>