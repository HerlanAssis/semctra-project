<template>
  <div class="app-container">
    <el-row class="page-container">
      <el-col style="margin: 10px 0 10px 0" class="text-center" :span="24">
        <typography convention="main-title">
          Atendimento
        </typography>
      </el-col>
      <el-col class="card-avatar" :span="24">
        <el-avatar :src="circleUrl" />
      </el-col>
      <el-col style="margin: 10px 0 10px 0" class="text-center" :span="24">
        <el-button @click="requestMeet">
          Solicitar Atendimetto
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Typography from '@/components/Typography'
import * as Meets from '@/api/meet'

export default {
  name: 'DashboardPatient',
  components: {
    Typography
  },
  data() {
    return {
      circleUrl: 'https://images.vexels.com/media/users/3/151709/isolated/preview/098c4aad185294e67a3f695b3e64a2ec-iacute-cone-de-avatar-do-m-eacute-dico-by-vexels.png'
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'avatar',
      'roles'
    ])
  },
  methods: {
    async requestMeet() {
      this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading'
      })

      this.$loading().close()

      const { data } = await Meets.save()

      console.log(data)

      if (data.id) {
        this.$router.push({ name: 'Meet', params: { id: data.id }})
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.card-avatar{
  display: flex;
  align-items: center;
  justify-content: center;

  .el-avatar {
    height: 300px;
    width: 300px;
  }
}
</style>
