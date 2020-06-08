<template>
  <div class="wrapper">
    <div id="login" v-if="!signup">
      <div class="form-header" :class="[badLogin ? 'bad-login' : '']">
        <h4 v-if="!badLogin">qPCR Dashboard</h4>
        <h4 v-if="badLogin">Invalid Credentials</h4>
      </div>
      <form class="form-credentials" @submit.prevent="submitLogin">
        <input type="text" id="Username" class="text-box" v-model="username" placeholder="Username" />
        <input
          type="password"
          class="text-box"
          v-model="password"
          placeholder="Password"
          @keypress.enter="submitLogin"
        />
      </form>
      <button type="submit" class="submit-button" @click="submitLogin" value="Sign In">Sign in</button>
      <button type="submit" class="submit-button" @click="signup=true" value="Sign Up">Sign up</button>
    </div>
    <div id="login" v-else>
      <div class="form-header">
        <h4>{{ titleSignup }}</h4>
      </div>
      <form class="form-credentials" @submit.prevent="submitSignup">
        <input type="text" id="Username" class="text-box" v-model="username" placeholder="Username" />
        <input type="email" class="text-box" v-model="email" placeholder="Email" />
        <input type="password" class="text-box" v-model="password" placeholder="Password" />
        <input
          type="password"
          class="text-box"
          v-model="password"
          placeholder="Confirm Password"
          @keypress.enter="submitSignup"
        />
      </form>
      <button type="submit" class="submit-button" @click="submitSignup=true" value="Sign Up">Sign up</button>
      <button
        type="submit"
        class="submit-button btn-grey"
        @click="signup=false"
        value="Sign In"
      >I Have an Account</button>
    </div>
  </div>
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
$GreyLight: #d8d8d8;
$Indicator: #539ee4;
$IndicatorLight: #7dbaf3;
$GreyDarker: #505050;
$ErrorColor: #cf5959;

.wrapper {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  min-height: 100%;
}

#login {
  -webkit-border-radius: 10px 10px 10px 10px;
  border-radius: 10px 10px 10px 10px;
  background: #fff;
  width: 90%;
  max-width: 450px;
  position: absolute;
  top: 200px;
  -webkit-box-shadow: 0 30px 60px 0 rgba(0, 0, 0, 0.3);
  box-shadow: 0 15px 60px 0 rgba(0, 0, 0, 0.3);
  text-align: center;

  a {
    color: $GreyDarker;
    border: none;
    text-decoration: none;

    &:hover {
      color: $Indicator;
    }
  }

  h4 {
    display: inline-block;
    text-align: center;
    font-size: 18px;
    font-weight: 500;
    text-transform: uppercase;
    margin: 5px;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
  }

  .bad-login {
    background: $ErrorColor !important;
    color: white;
  }

  .form-header {
    color: white;
    font-weight: 300;
    border-bottom: 1px solid #dce8f1;
    background-color: $Indicator;
    padding: 15px;
    text-align: center;
    border-radius: 10px 10px 0px 0px;
    transition: all 0.3s ease-in-out;
  }

  .form-footer {
    background-color: #f6f6f6bd;
    border-top: 1px solid #dce8f1;
    padding: 15px;
    text-align: center;
    border-radius: 0 0 10px 10px;
  }

  .submit-button {
    background: $Indicator;
    color: #fff;
    border: none;
    padding: 10px 50px;
    border-radius: 5px;
    margin: 5px 5px 20px 5px;
    text-transform: uppercase;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    font-size: 14px;
    box-shadow: 0 10px 30px 0 #00843e65;
    -webkit-box-shadow: 0 10px 30px 0 #02507465;
    -webkit-transition: all 0.2s ease-in-out;
    -webkit-border-radius: 5px;
    -moz-transition: all 0.2s ease-in-out;
    -ms-transition: all 0.2s ease-in-out;
    -o-transition: all 0.2s ease-in-out;
    transition: all 0.2s ease-in-out;
    cursor: pointer;

    &:hover {
      background: $IndicatorLight;
    }

    &:active {
      -moz-transform: scale(0.9);
      -webkit-transform: scale(0.9);
      -o-transform: scale(0.9);
      -ms-transform: scale(0.9);
      transform: scale(0.9);
    }
  }

  .btn-green {
    background: #00843ec4;

    &:hover {
      background: #0d9e51a2;
    }
  }

  .btn-grey {
    background: #393d3bd0;

    &:hover {
      background: #3335339f;
    }
  }

  .form-credentials {
    margin: 15px;

    .text-box {
      border: none;
      color: $GreyDarker;
      padding: 15px 30px;
      border-radius: 5px;
      border: 2px solid $GreyLight;
      margin: 15px 5px 0px 5px;
      font-size: 18px;
      text-align: center;
      width: 60%;
      transition: all 0.5s ease-in-out;

      &:focus {
        background-color: #fff;
        border-bottom: 2px solid $IndicatorLight;
      }

      &:placeholder {
        color: #a7a7a7;
      }
    }
  }

  .form-footer {
    border-top: 1px solid $GreyLight;
  }
}
</style>