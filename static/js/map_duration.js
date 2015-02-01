/**
 * Generates simple time series graph to show changes in duration for each map
 */

// $(function () {
//   var map_duration = new Highcharts.Chart({
//     chart: {renderTo: 'map_duration',
//            type: 'line',
//            zoomType: 'x',
//            resetZoomButton: {position: {x: 0, y: -30}}},
//     title: {'text': "Match Duration over Time for different Maps"},
//     xAxis: {'type': 'datetime', 'title': {'text': 'Date'}},
//     yAxis: {'title': {'text': 'Game Duration (in seconds)'}, "min": 0},
//     series: [{'name': 'yoloyolo', 'data': [[0,0],[1,1],[2,2]]},
//       {'name': 'tehehehehe', 'data': [[0.1,2], [1.2, 1.5], [3,1]]}]
//   });
// });

$(document).ready(function() {
  var options = {
    chart: {renderTo: 'map_duration',
           type: 'line',
           zoomType: 'x',
           resetZoomButton: {position: {x: 0, y: -30}}},
    title: {'text': "Match Duration over Time for different Maps"},
    xAxis: {'type': 'datetime', 'title': {'text': 'Date'}},
    yAxis: {'title': {'text': 'Game Duration (in seconds)'}, "min": 0},
    series: []
  };
  $.getJSON('/api/duration', function(list) {
    options.series.push(list);
    var map_duration = new Highcharts.Chart(options);
    console.log(map_duration)
  });
});
