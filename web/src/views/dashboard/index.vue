<template>
  <div class="app-container">
    <component :is="currentRole" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import HealthProfessional from './health_professional'
import Patient from './patient'

export default {
  name: 'Dashboard',
  components: { HealthProfessional, Patient },
  data() {
    return {
      currentRole: 'HealthProfessional'
    }
  },
  computed: {
    ...mapGetters([
      'roles'
    ])
  },
  created() {
    if (!this.roles.includes('HEALTH_PROFESSIONAL')) {
      this.currentRole = 'Patient'
    }
  }
}
</script>
