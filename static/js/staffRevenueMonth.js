google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

const mdirect0 = mdirect[0];
const mindirect0 = mindirect[0];

function drawChart() {
  var data = google.visualization.arrayToDataTable([
    ['Sales', 'Amount'],
    ['Bought by customer', mdirect0],
    ['Bought via agent', mindirect0],
  ]);

  var options = {
    title: 'Total Revenue Last Month'
  };

  options.colors = ["#6ec6ca", "#0598aa"];
  var chart = new google.visualization.PieChart(document.getElementById('revenueMonth'));

  chart.draw(data, options);
}
