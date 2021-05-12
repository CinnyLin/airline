google.charts.load('current', {'packages': ['geochart'],
'mapsApiKey': 'AIzaSyDMBKsxrynlg8azM7OH5RGkTU6YLI83S38'});
google.charts.setOnLoadCallback(drawMarkersMap);

const dest0 = new_dest;
const tickets0 = new_tickets;

function drawMarkersMap() {
    var d= [];
    var Header = ["Destination", "#tickets"];
    d.push(Header);
    for (var i=0; i<dest0.length; i++){
        var temp=[];
        temp.push(dest0[i]);
        temp.push(tickets0[i]);
        d.push(temp)
    }

var data = google.visualization.arrayToDataTable(d);

var options = {
displayMode: 'markers',
colorAxis: {colors: ['#0598aa']}
};

var chart = new google.visualization.GeoChart(document.getElementById('topDestinationsMonth'));
chart.draw(data, options);
};