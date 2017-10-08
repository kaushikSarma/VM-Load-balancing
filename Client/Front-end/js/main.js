(function($){
    var GLOBALS = {
        nservers: 0,
        updateInterval: 1000,
        dataLength: 20,
        servers: {}
    },
    CPUGraphs = {
        container: null,
        charts: [],        
        dps: [],
        xVal: 0
    },
    MEMGraphs = {
        container: null,
        charts: [],
        dps: [],
        xVal: 0
    },
    ServerRequest = {
        request: function(id){
            data = $.ajax({
                request: 'GET',
                url: 'http://localhost:8070/stats?id='+id,
                async: false,
                success: function(status){
                },
                failure: function(status){
                }
            }).responseText;
            console.log(data);
            data = JSON.parse(data);
            return data;
        },
        requestNumServers: function(){
            data = $.ajax({
                request: 'GET',
                url: 'http://localhost:8070/numservers',
                async: false,
                success: function(status){
                },
                failure: function(status){
                }
            }).responseText;
            data = JSON.parse(data)['n'];
            console.log("Number of servers = " + data)
            return data;
        }
    },
    PopulateCharts = function(category, type){
        category.container = $('#' + type + 'ChartContainer');
        for(i=1; i <= GLOBALS.nservers; i++){
            category.container.append('<div class="chart" id="' + type + 'Chart' + i + '"></div>');
            category.dps[i] = []
            category.charts[i] = new CanvasJS.Chart(type + "Chart" + i, {
                    title :{
                        text: type + " Server " + i 
                    },
                    axisY: {
                        includeZero: false
                    },      
                    data: [{
                        type: "area",
                        dataPoints: category.dps[i],
                        valueFormatString: ' '
                    }]
                });
        }
    },
    UpdateCharts = function(category, chartid, y){
        console.log(chartid, y);
        yVal = y;
        category.dps[chartid].push({
            x: category.xVal,
            y: yVal
        });
        category.xVal = category.xVal + 1;

        if (category.dps[chartid].length > GLOBALS.dataLength) {
            category.dps[chartid].shift();
        }
        category.charts[chartid].render();
    };
    $(document).ready(function(){
        GLOBALS.nservers = ServerRequest.requestNumServers();
        PopulateCharts(CPUGraphs, 'cpu');
        PopulateCharts(MEMGraphs, 'mem');
        setInterval(function(){
            GLOBALS.servers = ServerRequest.request(0);
            for (var key in GLOBALS.servers) {
                UpdateCharts(CPUGraphs, key, GLOBALS.servers[key].cpu);
                UpdateCharts(MEMGraphs, key, GLOBALS.servers[key].cpu);
            }
        }, GLOBALS.updateInterval);    
    });
})(jQuery);