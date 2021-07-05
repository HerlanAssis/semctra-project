<template>
  <div>
    <panel-group @handleSetLineChartData="handleSetLineChartData" />

    <el-row v-if="getNextPatient" :gutter="0" class="page-container">
      <el-col class="card-info card-avatar" :span="3">
        <el-avatar size="small" :src="circleUrl" />
      </el-col>

      <el-col class="card-info patient-detail" :span="17">
        <el-row>
          <el-col :span="12">
            <typography convention="small-title">
              Nome: <typography convention="title">{{ getNextPatient.username }}</typography>
            </typography>
          </el-col>
          <el-col :span="12">
            <typography convention="small-title">
              Idade: <typography convention="title">50 anos</typography>
            </typography>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="24">
            <typography convention="title">
              Motivo do Atendimento:
            </typography>
          </el-col>
          <el-col :span="24">
            <typography>
              Paciente diz sentir fortes dores na cabeça, tontoras e enjoos.
            </typography>
          </el-col>
        </el-row>

      </el-col>

      <el-col class="card-info card-action" :span="4">
        <div class="card-action-icon-wrapper icon-phone-call" @click="getNextMeet">
          <svg-icon icon-class="phone-call" class-name="card-action-icon" />
        </div>

        <!-- TODO: modal com dados clíncos do paciente  -->
        <div class="card-action-icon-wrapper icon-more">
          <svg-icon icon-class="more" class-name="card-action-icon" />
        </div>
      </el-col>
    </el-row>

    <el-row>
      <el-table
        v-loading="queue.loading"
        :data="getQueueList"
        border
        fit
        highlight-current-row
        style="width: 100%;"
      >

        <el-table-column min-width="220px" align="center" label="Fila">
          <template slot-scope="{row}">
            <span>
              {{ row.requester.username }}
            </span>
          </template>
        </el-table-column>

        <el-table-column fixed="right" min-width="45px" align="center" label="Ações">
          <template slot-scope="{row}">
            <el-button type="primary" size="mini" icon="el-icon-paper" @onClick="handeDetail(row)">
              Detalhes
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>

</template>

<script>
import { mapGetters } from 'vuex'
import PanelGroup from '../components/PanelGroup'
import Typography from '@/components/Typography'
import * as Meets from '@/api/meet'
import * as Queue from '@/api/queue'
import { NotificationMixin } from '../mixin'

export default {
  name: 'DashboarHealthProfessional',
  components: {
    Typography,
    PanelGroup
  },
  mixins: [NotificationMixin],
  data() {
    return {
      circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      meets: {
        loading: false,
        list: []
      },
      queue: {
        loading: false,
        list: []
      }
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'avatar',
      'roles'
    ]),
    dataList() {
      return this.queue.list
    },
    loading() {
      return this.meets.loading
    },
    getNextPatient() {
      let patient = false

      if (this.queue.list.length > 0) patient = this.queue.list[0]?.requester

      return patient
    },
    getQueueList() {
      let queueList = []

      if (this.queue.list.length > 0) queueList = this.queue.list.slice(1)

      return queueList
    }
  },
  watch: {
    loading(newVal) {
      if (newVal) {
        this.$loading({
          lock: true,
          text: 'Loading',
          spinner: 'el-icon-loading'
        })
      } else {
        this.$loading().close()
      }
    }
  },
  created() {
    this.checkScheduleMessage()
  },
  methods: {
    getData() {
      this.getQueueData()
    },
    getQueueData() {
      this.queue.loading = true
      Queue.getList().then(response => {
        this.queue.list = response.data
      }).finally(() => {
        this.queue.loading = false
      })
    },
    handleSetLineChartData(type) {
      // this.lineChartData = lineChartData[type]
    },
    async getNextMeet() {
      const { data } = await Meets.save()
      if (data.id) {
        this.$router.push({ name: 'Meet', params: { id: data.id }})
      }
    },
    handeDetail() {

    },
    checkScheduleMessage() {
      this.$confirm('Seu cronograma de atendimento está atualizado?', 'Verificação de Cronograma', {
        confirmButtonText: 'Sim',
        cancelButtonText: 'Não',
        type: 'warning'
      }).then(() => {
        this.$message({
          type: 'success',
          message: 'Ótimo, sempre mantenha o seu cronograma atualizado :D'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: 'Entendido, poderia atualizá-lo agora?'
        })
        this.$router.push({ name: 'Cronograma' })
      })
    },
    showPushNotification() {
      this.$notify({
        title: 'Fila de atendimentos',
        message: 'A fila de atendimento foi atualizada!',
        type: 'info'
      })
    }
  }
}
</script>

<style lang="scss" scoped>

.card-info {
  height: 100px;
}

.card-avatar {
  display: flex;
  align-items: center;
  justify-content: center;

  .el-avatar {
    height: 90px;
    width: 90px;
  }
}

.card-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-left: 10px !important;

  .icon-phone-call {
    color: #40c9c6;

    &:hover {
      cursor: pointer;
      color: white;
      background: #40c9c6;
    }
  }

  .icon-more {
    color: #36a3f7;

    &:hover {
      cursor: pointer;
      color: white;
      background: #36a3f7;
    }

    transform: rotate(90deg);
  }

  .card-action-icon-wrapper {
    float: left;
    margin: 14px 0 0 14px;
    padding: 16px;
    transition: all 0.38s ease-out;
    border-radius: 40px;
  }

  .card-action-icon {
    float: left;
    font-size: 48px;
  }

}

.patient-detail {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  padding: 0 0 10px 10px !important;

  border: 1px solid #DFE6EC;
  border-top: 0;
  border-bottom: 0;
}
</style>
