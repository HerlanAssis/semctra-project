<template>
  <div class="page-container">
    <el-row class="filter-container">
      <el-col style="display:flex; justify-content:flex-end" :span="24" :xs="24">
        <template>
          <el-tooltip
            class="item"
            effect="dark"
            :content="getQueue?'Já existe uma solicitação pendente':'Solicitar novo atendimento'"
            placement="top-end"
          >
            <span>
              <el-button
                :disabled="getQueue"
                type="primary"
                icon="el-icon-plus"
                @click="requestMeet"
              >
                Solicitar Atendimento
              </el-button>
            </span>
          </el-tooltip>
        </template>
      </el-col>
    </el-row>

    <el-row v-if="getMeet" style="margin: 10px 0 50px 0">
      <el-col style="margin: 10px 0" class="text-center" :span="24">
        <typography convention="main-title">
          Atendimento
        </typography>
      </el-col>
      <el-col class="card-avatar" :span="24">
        <el-avatar :src="circleUrl" />
      </el-col>
      <el-col style="margin: 10px 0" class="text-center" :span="24">
        <el-button icon="el-icon-phone-outline" type="primary" @click="handleBeginMeet(getMeet)">
          Entrar
        </el-button>
      </el-col>
    </el-row>

    <el-divider content-position="center">
      <typography convention="main-title">
        Solicitações
      </typography>
    </el-divider>

    <el-row>
      <el-table
        v-loading="queue.loading"
        :data="queue.list"
        border
        fit
        highlight-current-row
        style="width: 100%;"
      >
        <el-table-column min-width="220px" align="center" label="Médico">
          <template slot-scope="{row}">
            <span>
              {{ row.requester.username }}
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
            <el-popconfirm
              title="Tem certeza disso?"
              confirm-button-text="Confirmar"
              cancel-button-text="Cancelar"
              icon="el-icon-info"
              icon-color="red"
              @onConfirm="handleCancelQueueSolicitation(row)"
            >
              <el-button
                slot="reference"
                type="danger"
                size="mini"
                icon="el-icon-delete"
              >
                Cancelar
              </el-button>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-row>

    <el-divider content-position="center">
      <typography convention="main-title">
        Histórico de Atendimentos
      </typography>
    </el-divider>

    <el-row>
      <el-table
        v-loading="meet.loading"
        :data="historicList"
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
            <el-button
              type="success"
              size="mini"
              icon="el-icon-document-copy"
              @click="handleAccessDocuments(row)"
            >
              Consultar Documentos
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
import { NotificationMixin } from '../mixin'

export default {
  name: 'DashboardPatient',
  components: {
    Typography
  },
  mixins: [NotificationMixin],
  data() {
    return {
      circleUrl: 'https://images.vexels.com/media/users/3/151709/isolated/preview/098c4aad185294e67a3f695b3e64a2ec-iacute-cone-de-avatar-do-m-eacute-dico-by-vexels.png',
      meet: {
        list: [],
        loading: false
      },
      queue: {
        list: [],
        loading: false
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
      return this.meet.list
    },
    historicList() {
      return this.meet.list.filter(meet => meet.status === 'Encerrada')
    },
    getMeet() {
      const meet = (this.meet.list.filter(meet => meet.status === 'Iniciada') || [])[0]

      return meet
    },
    getQueue() {
      const queue = (this.queue.list.filter(queue => queue.status === 'Em processamento') || [])[0]

      return queue
    }
  },
  methods: {
    getData() {
      this.getMeetList()
      this.getQueueData()
    },
    requestMeet() {
      this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading'
      })

      Queue.save()
        .then(() => {
          this.$notify({
            title: 'Nova solicitação',
            message: 'Novo atendimento Solicitado com sucesso!',
            type: 'success'
          })
        })
        .finally(() => this.$loading().close())

      // if (data.id) {
      //   this.$router.push({ name: 'Meet', params: { id: data.id }})
      // }
    },
    async getQueueData() {
      const { data } = await Queue.getList()
      this.queue.list = data
    },
    async getMeetList() {
      const { data } = await Meet.getList()
      this.meet.list = data
    },
    handleBeginMeet(row) {
      this.$router.push({ name: 'Meet', params: { id: row.id }})
    },
    handleCancelQueueSolicitation(row) {
      Queue.remove(row).then(() => {
        this.$notify({
          title: 'Solicitação cancelada',
          type: 'warning'
        })
      })
    },
    handleAccessDocuments(row) {
      console.log(row)
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
