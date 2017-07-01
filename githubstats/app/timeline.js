function loadJSON(callback) {
  var xobj = new XMLHttpRequest();
  xobj.overrideMimeType("application/json");
  xobj.open("GET", "data/timeline.json", true);
  // Replace 'my_data' with the path to your file
  xobj.onreadystatechange = function() {
    if (xobj.readyState == 4 && xobj.status == "200") {
      // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
      callback(xobj);
    }
  };
  xobj.send(null);
}

function pad(n){return n<10 ? '0'+n : n}

function init() {
  loadJSON(function(response) {
    // Parse JSON string into object
    var actual_JSON = JSON.parse(response.responseText);
    var timelineText = document.getElementById("timeline");
    var yearmonth = "0000-00";
    var contents = "";

    for (x in actual_JSON) {
      var d = new Date(actual_JSON[x].time);
      var year = d.getFullYear();
      var month = pad(d.getMonth() + 1);
      var day = pad(d.getDate());

      var datestring = year + "-" + month + "-" + day;
      var newyearmonth = year + "-" + month;
      // close table when yearmonth changes, expect the
      // first time.
      if (yearmonth != newyearmonth && yearmonth != "0000-00") {
        contents += "\n\n\n</div>\n<!--closing table when yearmonth-->\n";
      };


      if (yearmonth !== newyearmonth) {
        contents += '<h2> ' + newyearmonth + '</h2> \n';
        contents += 
            '<div class="table">' +
            '  <div class="th">' +
            '    <div class="td">time</div>' +
            '    <div class="td">repo</div>' +
            '    <div class="td">action</div>' +
            '    <div class="td">target</div>' +
            '    <div class="td">message</div>' +
            '  </div>';
      }
      yearmonth = newyearmonth;


      contents +=
        '<div class="tr">\n ' +
        '<div class="td">' + datestring + "</div>" +
        '<div class="td">' + actual_JSON[x].repo + "</div>" +
        '<div class="td">' + actual_JSON[x].action + "</div>" +
        '<div class="td">' + actual_JSON[x].target + "</div>" +
        '<div class="td">' + actual_JSON[x].message.slice(0,100) + "</div>" +
        "</div>\n" 
    }
    timelineText.innerHTML += contents;
  });
}
