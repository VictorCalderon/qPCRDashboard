<template>
  <b-container>
    <div class="singin-body mt-5">
      <form class="form-signin text-center mt-5" @submit.prevent="submitLogin">
        <img class="mb-4" src="@/assets/qpcr.png" alt width="256" height="256" />
        <h1 class="h3 mb-3 font-weight-normal">Please sign in</h1>
        <label for="inputUsername" class="sr-only">Username</label>
        <input
          type="text"
          id="inputUsername"
          class="form-control text-center"
          placeholder="Username"
          required
          autofocus
          v-model="username"
        />
        <label for="inputPassword" class="sr-only">Password</label>
        <input
          type="password"
          id="inputPassword"
          class="form-control text-center"
          placeholder="Password"
          v-model="password"
          required
          @keypress.enter="submitLogin"
        />
        <button
          class="btn btn-lg btn-secondary btn-block"
          type="submit"
          @click="submitLogin"
          value="Sign In"
        >Sign in</button>
        <p class="mt-5 mb-3 text-muted">&copy; 2020</p>
      </form>
    </div>
  </b-container>
</template>


<script>
import router from "@/router/index";

export default {
  data() {
    return {
      signup: false,
      username: null,
      password: null,
      email: null,
      confirmPassword: null,
      badLogin: null
    };
  },
  methods: {
    submitLogin() {
      if (this.username && this.password) {
        this.postLogin();
      }
    },
    submitSignup() {
      if (
        this.username &&
        this.password &&
        this.password == this.confirmPassword &&
        this.email
      ) {
        this.postSigup();
      }
    },
    postLogin() {
      this.$store
        .dispatch("authLogin", {
          username: this.username,
          password: this.password
        })
        .then(() => {
          if (this.$route.name != "Dashboard") {
            router.push({
              name: "Dashboard"
            });
          }
        });
    },
    postSignup() {
      this.$store.dispatch("authSignUp", {
        username: this.username,
        password: this.password,
        email: this.email
      });
    }
  },
  computed: {
    logInError() {
      if (this.$store.getters.loginError) return this.$store.getters.loginError;
      else return null;
    },

    titleSignup() {
      if (this.$store.getters.loginError) return this.$store.getters.loginError;
      else return "SARS-CoV-2 Dashboard";
    }
  },
  watch: {
    logInError() {
      this.badLogin = true;
      setTimeout(() => {
        this.badLogin = false;
      }, 1500);
    }
  }
};
</script>

<style lang="scss" scoped>
.bd-placeholder-img {
  font-size: 1.125rem;
  text-anchor: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

@media (min-width: 768px) {
  .bd-placeholder-img-lg {
    font-size: 3.5rem;
  }
}

.signin-body {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
  text-align: center;
}

.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}
.form-signin .checkbox {
  font-weight: 400;
}
.form-signin .form-control {
  position: relative;
  box-sizing: border-box;
  height: auto;
  padding: 10px;
  font-size: 16px;
}
.form-signin .form-control:focus {
  z-index: 2;
}
.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}
.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>