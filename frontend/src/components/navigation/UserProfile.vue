<template>
  <div id="Profile">
    <div class="user-profile">
        <div class="user-name"><i class="fas fa-user"></i>&nbsp;{{ currentUser.name }}</div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
        currentUser: {
            name: 'Victor Calderon'
        }
    };
  },
  methods: {
    openProfile() {
      this.$store.dispatch("openProfile");
    }
  }
};
</script>

<style lang="scss">
$GreyLight: #d8d8d8;
$GreyDark: #969696;
$GreenRef: #00843d;
$GreenRefDark: #005c2b;
$GreenRefLight: #01a34d;
$GreyDarker: #505050;
$GreyBackground: #e6e6e6;
$GreyBackgroundDark: #535353;
$Indicator: #539ee4;

#Profile {
    margin-top: 10px;

    .user-profile {
        display: block;
        color: white;
        background: $GreyBackgroundDark;
        height: 50px;
        border-radius: 5px;

    .user-name {
        display: block;
        color: white;
        font-size: 1.6rem;
        font-weight: 400;
        transition: all 0.2s ease-in-out;
        -webkit-transition: all 0.2s ease-in-out;
        -moz-transition: all 0.2s ease-in-out;
        text-decoration: none;
        cursor: pointer;

        .fas {
            color: $GreyBackground;
            font-size: 2rem;
            margin-top: 8px;
            margin-right: 10px;
            margin-left: 10px;
            }

        &:hover {
            // background: $GreyDarker;
            color: white;
            font-weight: 300;

            .fa {
            color: white;
            }

            .fas {
            color: white;
            }
        }
    }
  }
}

#routerView {
  text-align: center;
}
</style>
