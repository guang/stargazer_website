/**
 * Generates simple time series graph to show changes in duration for each map
 */

$(document).ready(function() {
  var options = {
    chart: {renderTo: 'duration_by_time',
           type: 'line',
           zoomType: 'x',
           resetZoomButton: {position: {x: 0, y: -30}}},
    title: {'text': "Match Duration over Time for different Maps"},
    xAxis: {'type': 'datetime', 'title': {'text': 'Date'}},
    yAxis: {'title': {'text': 'Game Duration (in seconds)'}, "min": 0},
    series: []
  };

  $("#submit_data").bind('click',function(event){
    var map_name = $("#map_name").val()
    var query_type = $("#query_type").val()
    fetch_map(map_name, query_type);
  });

function fetch_map(map_name, query_type) {
  $.getJSON('/api/' + map_name + '/' + query_type + '/A/', function(list) {
    options.series.push(list);
    var map_duration = new Highcharts.Chart(options);
  });
}


});
