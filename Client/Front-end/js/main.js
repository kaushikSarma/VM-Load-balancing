function request(id){
    data = $.ajax({
        request: 'GET',
        url: 'http://localhost:8070/stats?id='+id,
        async: false,
        success: function(status){
        },
        failure: function(status){
        }
    }).responseText;
    data = JSON.parse(data);
    return data;
}

function requestNumServers(){
    data = $.ajax({
        request: 'GET',
        url: 'http://localhost:8070/numservers',
        async: false,
        success: function(status){
        },
        failure: function(status){
        }
    }).responseText;
    return JSON.parse(data)['i'];
}

window.onload = function () {
    nservers = requestNumServers();
    
    var xVal = 0;
    var yVal = 100; 
    var updateInterval = 300;
    var dataLength = 20; // number of dataPoints visible at any point
    
    chartContainer = $('#chartContainer');

    console.log(chartContainer);
    charts = [];
    dps = []
    
    for(i=1; i <= nservers; i++){
        chartContainer.append('<div class="chart" id="chart' + i + '"></div>');
        dps[i] = []
        charts[i] = new CanvasJS.Chart("chart" + i, {
                title :{
                    text: "CPU Server " + i 
                },
                axisY: {
                    includeZero: false
                },      
                data: [{
                    type: "area",
                    dataPoints: dps[i]
                }]
            });
    }

    var updateChart = function (chartid, y) {
        count = 1;
        console.log(chartid, y);
        for (var j = 0; j < count; j++) {
            // yVal = yVal +  Math.round(5 + Math.random() *(-5-5));
            yVal = y;
            dps[chartid].push({
                x: xVal,
                y: yVal
            });
            xVal = xVal + 1;
        }

        if (dps[chartid].length > dataLength) {
            dps[chartid].shift();
        }
        charts[chartid].render();
    };
    
    setInterval(function(){
        servers = request(0);
        for (var key in servers) {
            updateChart(key, servers[key].cpu);
        }
    }, updateInterval);
}