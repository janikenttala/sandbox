function loadJSON(data, config, callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', data, true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(config, xobj.responseText);
        }
    };
    xobj.send(null);
}

function myCallback(config, response) {
    // Parse JSON string into object
    var jsonfile = JSON.parse(response);

    // Map labels and values from json to form the chart expects.
    var datamodel = config.data_model;
    // Get values
    var datasets = [];
    for (let i = 0; i < datamodel["values"].length; i++) {
        var dataset = {};
        var name = datamodel.values[i];

        // this is the format chart wants
        dataset.label = name;
        dataset.data = jsonfile.map(function (e) {return e[name];});
        dataset.backgroundColor = datamodel.colors[i];
        datasets.push(dataset);
    }
    var labels = jsonfile.map(function (e) {return e[datamodel["label"]];});

    var ctx = document.getElementById("line-chart");
    var config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: config.chart_title
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    display: true,
                    time: {
                        unit: time_interval,
                        displayFormats: display_formats

                    },
                    scaleLabel: {
                        display: true,
                        labelString: x_label
                    },
                    ticks: {
                        major: {
                            fontStyle: 'bold',
                            fontColor: '#FFFF00'
                        }
                    }
                }],
                yAxes: [{
                    display: true,
                    stacked: stacked,
                    scaleLabel: {
                        display: true,
                        labelString: y_label
                    }
                }]
            }
        }
    };

    var chart = new Chart(ctx, config);
}


for (var key in configx) {
    let chart_id = key;
    let data_file = configx[key]["data_file"];
    let config = configx[chart_id];
    loadJSON(data_file, config, myCallback);

}