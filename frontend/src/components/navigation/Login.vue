Indicator;
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