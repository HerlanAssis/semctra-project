<template>
  <div class="components-container">
    <!-- <el-row>
      <el-col class="text-center" :span="24">
        <h1 styles="text-align: center;">Meet</h1>
      </el-col>
    </el-row> -->

    <div id="mural" style="height: 75vh;" />

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import * as Meets from '@/api/meet'

const VUE_APP_JITSI_SCRIPT_URL = process.env.VUE_APP_JITSI_SCRIPT_URL
const VUE_APP_JITSI_DOMAIN_URL = process.env.VUE_APP_JITSI_DOMAIN_URL

export default {
  name: 'DashboardEditor',
  data() {
    return {
      api: null
    }
  },
  computed: {
    ...mapGetters([
      'user'
    ])
  },
  mounted() {
    // As an instance method inside a component
    this.$loadScript(VUE_APP_JITSI_SCRIPT_URL).then(() => {
      Meets.get({ id: this.$route.params?.id }).then(response => {
        const meet = response.data
        const options = {
          roomName: meet.pin,
          jwt: meet.token,
          parentNode: document.querySelector('#mural'),
          userInfo: {
            email: this.user.email,
            displayName: this.user.name
          }
        }
        this.api = new JitsiMeetExternalAPI(VUE_APP_JITSI_DOMAIN_URL, options)
        this.api.executeCommand('setVideoQuality', 480);
      })
    }).catch(err => {
      // Failed to fetch script
      console.log(err)
    })
  },
  beforeDestroy() {
    // As an instance method inside a component
    this.$unloadScript(VUE_APP_JITSI_SCRIPT_URL).then(() => {
      this.api?.executeCommand('hangup')
      document.querySelector('#mural').removeChild(this.api.getIFrame())
    })
  },
  methods: {

  }
}
</script>

