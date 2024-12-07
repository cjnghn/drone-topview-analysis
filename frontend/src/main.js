import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import "./style.css";

const app = createApp(App);
app.config.globalProperties.$axios = axios.create({
  baseURL: "http://localhost:8000/api/v1/",
});
app.mount("#app");
