import { createStore } from 'vuex'
import auth from './modules/auth'
import patients from './modules/patients'
import appointments from './modules/appointments'
import imaging from './modules/imaging'
import chatbot from './modules/chatbot'
import ai from './modules/ai'
import users from './modules/users'
import medicalRecords from './modules/medicalRecords'
import prescriptions from './modules/prescriptions'

export default createStore({
  modules: {
    auth,
    patients,
    appointments,
    imaging,
    chatbot,
    ai,
    users,
    medicalRecords,
    prescriptions
  }
})