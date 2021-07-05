export const NotificationMixin = {
  created: function() {
    this.getData()

    // atualiza a lista a cada 15 segundos
    setInterval(this.getData, 15 * 1000)
  },
  watch: {
    dataList: function(prevValue, newValue) {
      if (prevValue.length !== newValue.length) {
        this.showPushNotification()
      }
    }
  },
  methods: {
    getData: function() {
      throw new Error('Essa função deve ser sobrescrita!')
    },
    showPushNotification() {
      throw new Error('Essa função deve ser sobrescrita!')
    }
  },
  computed: {
    dataList() {
      throw new Error('Essa função deve ser sobrescrita!')
    }
  }
}
