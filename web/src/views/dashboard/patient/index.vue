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

    <el-row>
      <el-table
        v-loading="meet.loading"
        :data="meet.list"
        border
        fit
        highlight-current-row
        style="width: 100%;"
      >

        <el-table-column min-width="220px" align="center" label="Médico">
          <template slot-scope="{row}">
            <span>
              {{ row.host.username }}
            </span>
          </template>
        </el-table-column>

        <el-table-column min-width="220px" align="center" label="Status">
          <template slot-scope="{row}">
            <span>
              {{ row.status }}
            </span>
          </template>
        </el-table-column>

        <el-table-column fixed="right" min-width="90px" align="center" label="Ações">
          <template slot-scope="{row}">
            <el-button :disabled="!row.token" type="success" size="mini" icon="el-icon-video-camera" @click="handleBeginMeet(row)">
              Chamada de Vídeo
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Typography from '@/components/Typography'
import * as Queue from '@/api/queue'
import * as Meet from '@/api/meet'

export default {
  name: 'DashboardPatient',
  components: {
    Typography
  },
  data() {
    return {
      circleUrl: 'https://images.vexels.com/media/users/3/151709/isolated/preview/098c4aad185294e67a3f695b3e64a2ec-iacute-cone-de-avatar-do-m-eacute-dico-by-vexels.png',
      meet: {
        list: [],
        loading: false
      }
    }
  },
  created() {
    this.getMeetList()
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

      await Queue.save()

      // if (data.id) {
      //   this.$router.push({ name: 'Meet', params: { id: data.id }})
      // }
    },
    async getMeetList() {
      const { data } = await Meet.getList()
      this.meet.list = data
    },
    handleBeginMeet(row) {
      this.$router.push({ name: 'Meet', params: { id: row.id }})
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
