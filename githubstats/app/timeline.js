 function loadJSON(callback) {   

  var xobj = new XMLHttpRequest();
  xobj.overrideMimeType("application/json");
  xobj.open('GET', 'data/timeline.json', true); 
  // Replace 'my_data' with the path to your file
  xobj.onreadystatechange = function () {
    if (xobj.readyState == 4 && xobj.status == "200") {
      // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
      callback(xobj);
    }
  };
  xobj.send(null);  
}
 
 function init() {
  loadJSON(function(response) {
    // Parse JSON string into object
    var actual_JSON = JSON.parse(response.responseText);
    var timelineText = document.getElementById('timeline');
    for (x in actual_JSON) {
      timelineText.innerHTML += "\n " + 
        actual_JSON[x].time + " " + 
        actual_JSON[x].repo + " " +
        actual_JSON[x].action + " " +
        actual_JSON[x].target + " " +
        actual_JSON[x].message
        ;
    }
  });
}
 
