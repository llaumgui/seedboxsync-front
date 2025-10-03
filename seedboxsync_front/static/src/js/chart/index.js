// Chart.js
import Chart from "chart.js/auto";
window.Chart = Chart;

import { createBarChart, loadChart } from "./create_bar";
window.createBarChart = createBarChart;
window.loadChart = loadChart;
