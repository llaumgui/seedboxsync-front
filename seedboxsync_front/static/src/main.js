// SASS
import "./scss/main.scss";

// VanillaJS
import "./js/bulma_notification.js";
import "./js/bulma_navbar.js";

// AlpineJS
import Alpine from "alpinejs";
window.Alpine = Alpine;
Alpine.start();

// Chart.js
import Chart from "chart.js/auto";
window.Chart = Chart;
document.addEventListener("DOMContentLoaded", () => {
  initChart();
});
