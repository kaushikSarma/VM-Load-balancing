(function($){
    var GLOBALS = {                             //  Global variables 
        nservers: 0,
        // url: 'http://localhost:8070/,
        url: 'http://192.168.2.107:8070/',
        updateInterval: 150,
        dataLength: 20,
        servers: {},
        currentID: 'cpu',
        currentCategory: null
    },
    CPUGraphs = {                               //  Wrapper object for CPU graphs, rendered in CanvasJS
        container: null,
        charts: [],        
        dps: [],
        xVal: 0,
        getY: function(chartid){
            return GLOBALS.servers[chartid].cpu;
        }
    },
    MEMGraphs = {                               //  Wrapper object for Memory graphs, rendered in CanvasJS
        container: null,
        charts: [],
        dps: [],
        xVal: 0,
        getY: function(chartid){
            return GLOBALS.servers[chartid].mem[2];            
        }
    },
    ServerRequest = {                           //  Wrapper for functions to send requests to query.py 
        request: function(id){                  //  Function to ajax request the stats from a server 
            data = $.ajax({
                request: 'GET',
                url: GLOBALS.url+'stats?id='+id,
                async: false,
                success: function(status){
                },
                failure: function(status){
                }
            }).responseText;
            // console.log(data);
            data = JSON.parse(data);
            return data;
        },
        requestNumServers: function(){          //  Function to ajax request the number of servers running 
            data = $.ajax({
                request: 'GET',
                // url: 'http://localhost:8070/numservers',
                url: GLOBALS.url + 'numservers',
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
    PopulateCharts = function(category, type){  //  Function to append corresponding charts
        category.container = $('#' + type + 'ChartContainer');
        for(i=1; i <= GLOBALS.nservers; i++){
            category.container.append('<div class="chart" id="' + type + 'Chart' + i + '"></div>');
            category.dps[i] = []
            category.charts[i] = new CanvasJS.Chart(type + "Chart" + i, {
                    title :{
                        text: "Server " + i 
                    },
                    axisY: {
                        includeZero: false,
                        maximum: 100,
                        minimum: 0
                    },      
                    axisX: {
                        tickLength: 0,
                        lineThickness: 0,
                        valueFormatString: " "
                    },
                    data: [{
                        type: "splineArea",
                        dataPoints: category.dps[i]
                    }]
                });
        }
    },
    UpdateCharts = function(category, chartid){  //  Function to push data points to charts and render the graph
        yVal = category.getY(chartid);
        category.dps[chartid].push({
            x: category.xVal,
            y: yVal
        });
        category.xVal = category.xVal + 1;

        if (category.dps[chartid].length > GLOBALS.dataLength) {
            category.dps[chartid].shift();
        }
        category.charts[chartid].render();
    },
    IntervalRequestLoop = null;

    $(document).ready(function(){
        GLOBALS.nservers = ServerRequest.requestNumServers();
        // GLOBALS.nservers = 1;
        GLOBALS.currentCategory = CPUGraphs;
        PopulateCharts(CPUGraphs, 'cpu');        
        PopulateCharts(MEMGraphs, 'mem');        

        ToggleRequestButton = $('#toggleRequest')
            .bind('click', function(){
                console.log('toggle', IntervalRequestLoop);
                if (IntervalRequestLoop !== null) {
                    console.log('stop', IntervalRequestLoop);
                    clearInterval(IntervalRequestLoop);
                    IntervalRequestLoop = null;
                    $(this).text('Start');
                }
                else {
                    $(this).text('Stop');                    
                    IntervalRequestLoop = setInterval(function(){
                        GLOBALS.servers = ServerRequest.request(0);
                        for (var key in GLOBALS.servers) {
                            UpdateCharts(GLOBALS.currentCategory, key);
                        }
                    }, GLOBALS.updateInterval);    
                }
            });

        var graphButtons = $('.changeGraph')
            .bind('click', function(){
                GLOBALS.currentID = $(this).attr('id');
                if(GLOBALS.currentID == 'cpu')  {
                    GLOBALS.currentCategory = CPUGraphs;
                    $('#memChartContainer').hide();
                    $('#cpuChartContainer').show();
                }
                else if(GLOBALS.currentID == 'mem')  {
                    GLOBALS.currentCategory = MEMGraphs;
                    $('#memChartContainer').show();
                    $('#cpuChartContainer').hide();
                }
            });
    });
})(jQuery);