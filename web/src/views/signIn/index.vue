<template>
  <div class="login-container">
    <el-form
      ref="loginForm"
      :model="loginForm"
      :rules="loginRules"
      class="login-form"
      autocomplete="on"
      label-position="top"
    >
      <div class="title-container">
        <h3 class="title">Cadastro</h3>
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="Username"
          name="username"
          type="text"
          autocomplete="on"
        />
      </el-form-item>

      <el-form-item prop="email">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="email"
          v-model="loginForm.email"
          placeholder="Email"
          name="email"
          type="text"
          autocomplete="on"
        />
      </el-form-item>

      <el-form-item prop="cpf">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="cpf"
          v-model="loginForm.cpf"
          v-mask="'###.###.###-##'"
          placeholder="CPF"
          name="cpf"
          type="text"
          autocomplete="on"
        />
      </el-form-item>

      <el-form-item prop="phone">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="phone"
          v-model="loginForm.phone"
          v-mask="'#######-####'"
          placeholder="Telefone"
          name="phone"
          type="text"
          autocomplete="on"
        />
      </el-form-item>

      <el-form-item prop="birthdate">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-date-picker
          ref="birthdate"
          v-model="loginForm.birthdate"
          v-mask="'##/##/####'"
          prefix-icon="null"
          placeholder="Data de Nascimento"
          name="birthdate"
          format="dd/MM/yyyy"
        />
      </el-form-item>

      <el-form-item label="Quem é você?" :prop="activeProfile">
        <el-tabs v-model="activeProfile" style="color: #fff" stretch @tab-click="handleChangeProfile">
          <el-tab-pane label="Paciente" name="sus_number">
            <el-input
              ref="patient"
              v-model="loginForm.sus_number"
              placeholder="Número do SUS"
              name="sus_number"
              type="text"
              autocomplete="on"
            />
          </el-tab-pane>
          <el-tab-pane label="Médico" name="crm">
            <el-input
              ref="patient"
              v-model="loginForm.crm"
              placeholder="Número do CRM"
              name="crm"
              type="text"
              autocomplete="on"
            />
          </el-tab-pane>
        </el-tabs>
      </el-form-item>

      <el-tooltip
        v-model="capsTooltip"
        content="Caps lock is On"
        placement="right"
        manual
      >
        <el-form-item prop="password">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="password"
            v-model="loginForm.password"
            :type="passwordType"
            placeholder="Senha"
            name="password"
            tabindex="2"
            autocomplete="on"
            @keyup.native="checkCapslock"
            @blur="capsTooltip = false"
            @keyup.enter.native="handleLogin"
          />
          <span class="show-pwd" @click="showPwd">
            <svg-icon
              :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"
            />
          </span>
        </el-form-item>
      </el-tooltip>

      <el-tooltip
        v-model="capsTooltip"
        content="Caps lock is On"
        placement="right"
        manual
      >
        <el-form-item prop="password_confirmation">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="confirm-password"
            v-model="loginForm.password_confirmation"
            :type="passwordType"
            placeholder="Confirmar Senha"
            name="confirm-password"
            tabindex="2"
            autocomplete="on"
            @keyup.native="checkCapslock"
            @blur="capsTooltip = false"
            @keyup.enter.native="handleLogin"
          />
          <span class="show-pwd" @click="showPwd">
            <svg-icon
              :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"
            />
          </span>
        </el-form-item>
      </el-tooltip>

      <div class="social-links">
        <el-button
          type="text"
          @click="handleClickLogin"
        >Já possui cadastro?</el-button>
        <el-button type="text">Esqueceu a senha?</el-button>
      </div>

      <el-button
        :loading="loading"
        type="primary"
        style="width:100%;margin-bottom:30px;"
        @click.native.prevent="handleSignIn"
      >Cadastrar</el-button>
    </el-form>

  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.loginForm.password) {
        callback(new Error('As senhas devem ser iguais!'))
      } else {
        callback()
      }
    }

    const validatePasswordComplexity = (rule, value, callback) => {
      const anUpperCase = /[A-Z]/
      const aLowerCase = /[a-z]/
      const aNumber = /[0-9]/

      if (value.length < 8) {
        callback(new Error('Deve ter 8 ou mais caracteres!'))
      } else if (!anUpperCase.test(value)) {
        callback(new Error('Deve ter um ou mais caracteres maiúsculos!'))
      } else if (!aLowerCase.test(value)) {
        callback(new Error('Deve ter um ou mais caracteres minúsculos!'))
      } else if (!aNumber.test(value)) {
        callback(new Error('Deve ter um ou mais caracteres numéricos!'))
      } else {
        callback()
      }
    }

    return {
      activeProfile: 'sus_number',
      loginForm: {
        username: '',
        email: '',
        cpf: '',
        phone: '',
        birthdate: '',
        sus_number: '',
        crm: '',
        password: '',
        password_confirmation: ''
      },
      loginRules: {
        username: [
          {
            required: true,
            trigger: 'blur',
            message: 'Este campo não pode ser vazio'
          }
        ],
        email: [
          {
            required: true,
            trigger: 'blur',
            type: 'email',
            message: 'Este campo não pode ser vazio'
          }
        ],
        cpf: [
          {
            required: true,
            trigger: 'blur',
            message: 'Este campo não pode ser vazio'
          }
        ],
        phone: [
          {
            required: true,
            trigger: 'blur',
            message: 'Este campo não pode ser vazio'
          }
        ],
        birthdate: [
          {
            required: true,
            trigger: 'blur',
            message: 'Este campo não pode ser vazio'
          }
        ],
        sus_number: [
          {
            required: true,
            trigger: 'blur',
            message: 'Este campo não pode ser vazio'
          }
        ],
        crm: [
          {
            required: true,
            trigger: 'blur',
            message: 'Este campo não pode ser vazio'
          }
        ],
        password: [
          {
            required: true,
            trigger: 'blur',
            message: 'Este campo não pode ser vazio'
          },
          {
            required: true,
            trigger: ['blur', 'change'],
            validator: validatePasswordComplexity
          }
        ],
        password_confirmation: [
          {
            required: true,
            trigger: ['blur', 'change'],
            validator: validateConfirmPassword
          }
        ]
      },
      passwordType: 'password',
      capsTooltip: false,
      loading: false,
      showDialog: false,
      redirect: undefined,
      otherQuery: {}
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        const query = route.query
        if (query) {
          this.redirect = query.redirect
          this.otherQuery = this.getOtherQuery(query)
        }
      },
      immediate: true
    }
  },
  created() {
    // window.addEventListener('storage', this.afterQRScan)
  },
  mounted() {
    if (this.loginForm.username === '') {
      this.$refs.username.focus()
    } else if (this.loginForm.password === '') {
      this.$refs.password.focus()
    }
  },
  destroyed() {
    // window.removeEventListener('storage', this.afterQRScan)
  },
  methods: {
    checkCapslock(e) {
      const { key } = e
      this.capsTooltip = key && key.length === 1 && key >= 'A' && key <= 'Z'
    },
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleSignIn() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true

          const data = Object.fromEntries(Object.entries(this.loginForm).filter(([k, v]) => !!v))
          data.birthdate = data.birthdate.toLocaleDateString()

          this.$store
            .dispatch('user/register', data)
            .then(() => {
              this.$router.push({
                path: this.redirect || '/',
                query: this.otherQuery
              })
              this.loading = false
            })
            .catch(() => {
              this.loading = false
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    getOtherQuery(query) {
      return Object.keys(query).reduce((acc, cur) => {
        if (cur !== 'redirect') {
          acc[cur] = query[cur]
        }
        return acc
      }, {})
    },
    handleClickLogin() {
      this.$router.push({
        name: 'login'
      })
    },
    handleChangeProfile() {
      this.loginForm.crm = ''
      this.loginForm.sus_number = ''
    }
  }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #283443;
$light_gray: #fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;

    &__label {
      color: #fff
    }
  }

  .el-tabs {
    &__item {
      color: #fff
    }
  }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 35px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .social-links {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 2rem;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }

  .thirdparty-button {
    position: absolute;
    right: 0;
    bottom: 6px;
  }

  @media only screen and (max-width: 470px) {
    .thirdparty-button {
      display: none;
    }
  }
}
</style>
