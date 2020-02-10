function loadJSON(callback) {

    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', 'data.json', true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText);
        }
    };
    xobj.send(null);
}
loadJSON(function (response) {
// Parse JSON string into object
console.log("YEAH")
var jsonfile = JSON.parse(response);
var labels = jsonfile.map(function (e) {
    return e.date;
});
var data = jsonfile.map(function (e) {
    return e.age;
});;

var pdata = jsonfile.map(function (e) {
    return e.page;
});;

var ctx = document.getElementById("line-chart")
var config = {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
                label: data_labels,
                data: data,
                backgroundColor: data_color
            },
            {
                label: data_labels,
                data: pdata,
                backgroundColor: "rgba(0, 51, 81, 0.9)"
            }
        ]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: chart_title
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

});
