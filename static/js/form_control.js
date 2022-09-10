//Fill in Origin Airport select
var select = document.getElementById("origin-iata");
var options = ["BOS", "LAX", "SFO", "DCA", "SLC"];

for(var i = 0; i < options.length; i++) {
    var opt = options[i];
    var el = document.createElement("option");
    el.textContent = opt;
    el.value = opt;
    select.appendChild(el);
}

// Fill in Destination Airport
var select = document.getElementById("destination-iata");
var options = ["BOS", "LAX", "SFO", "DCA", "SLC"];

for(var i = 0; i < options.length; i++) {
    var opt = options[i];
    var el = document.createElement("option");
    el.textContent = opt;
    el.value = opt;
    select.appendChild(el);
}