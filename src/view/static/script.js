var isSelect = false;
var setOriginFlag = false;
var setDestFlag = false;
var originCoords = "";
var destCoords = "";
var textOriginAddress = "";
var textDestAddress = "";
var pathLimit = 0;

var shortestDistance = 0;
var elevationDistance = 0;
var elevationDrop = 0
var elevationGain = 0;
var shortestDrop = 0;
var shortestGain = 0;


function roundOff(N){
    return Math.round(N*10000)/10000;
};

function setMapMarker(type, e) {
    if (type == "origin") {
        document.getElementById("origin").innerHTML = roundOff(e.lngLat["lat"])+","+roundOff(e.lngLat["lng"]);
        var m = new mapboxgl.Marker({color: "green"}).setLngLat(e.lngLat).addTo(map);
        return m;
    } else if (type == "dest") {
        document.getElementById("dest").innerHTML = roundOff(e.lngLat["lat"])+","+roundOff(e.lngLat["lng"]);
        var m = new mapboxgl.Marker({color: "red"}).setLngLat(e.lngLat).addTo(map);
        return m;
    }
}

function disableAddressFields(val){
    document.getElementById("textOriginAddress").disabled = val;
    document.getElementById("textDestAddress").disabled = val;
};

function resetParameters() {
    isSelect = false;
    setOriginFlag = false;
    setDestFlag = false;
    originCoords = "";
    destCoords = "";
    textOriginAddress = "";
    textDestAddress = "";
    pathLimit = 0;
    points = turf.featureCollection([]);
    map.getSource('circleData').setData(points);

    if (originMarker) {
        originMarker.remove();
    }
    if (destMarker) {
        destMarker.remove();
    }
    document.getElementById("textOriginAddress").value = "";
    document.getElementById("textDestAddress").value = "";
    document.getElementById("pathLimit").value = 0;
    document.getElementById("origin").innerHTML = "";
    document.getElementById("dest").innerHTML = "";

    disableAddressFields(false);

    resetOutputs();
}

function resetOutputs() {
    document.getElementById("shortestDistance").innerHTML = "";
    document.getElementById("elevationDistance").innerHTML = "";
    document.getElementById("gainShort").innerHTML = "";
    document.getElementById("gainDrop").innerHTML = "";
    document.getElementById("elev_path_gain").innerHTML = "";
    document.getElementById("elev_path_drop").innerHTML = "";

    elevationDistance = 0;
    shortestDistance = 0;
    elevationGain = 0;
    elevationDrop = 0
    shortestGain = 0;
    shortestDrop = 0;

    if (map.getLayer("shortest_route")) {
        map.removeLayer("shortest_route")
    }
    if (map.getSource("shortest_route")) {
        map.removeSource("shortest_route")
    }
    if (map.getLayer("ele_route")) {
        map.removeLayer("ele_route")
    }
    if (map.getSource("ele_route")) {
        map.removeSource("ele_route")
    }
}

document.getElementById("manual").onclick = function(){
    disableAddressFields(false);
    isSelect = false;
};

document.getElementById("select").onclick = function(){
    disableAddressFields(true);
    isSelect = true;
};

document.getElementById("reset").onclick = function(){
    resetParameters();
};

document.getElementById("submit").onclick = function(){
    var algorithm = $('input[name="algorithm"]:checked').val();
    var minMaxElevation = $('input[name="elevation"]:checked').val();
    pathLimit = document.getElementById("pathLimit").value;

    if(isSelect) {
        var submitData = {
            "origin_coords": originCoords,
            "dest_coords": destCoords,
            "min_max": minMaxElevation.toString(),
            "algorithm": algorithm.toString(),
            "path_limit": pathLimit
        }

        submitData = JSON.stringify(submitData);

        console.log(submitData);

        $.ajax({
            type: "POST",
            url: "/path_via_pointers",
            data: submitData,
            success: function(data) {
                plotRoute(data, "select")
                updateOutputs(data)
            },
            dataType: "json"
        });
    } else if (!isSelect) {
        var submitData = {
            "text_origin_address": textOriginAddress,
            "text_dest_address": textDestAddress,
            "min_max": minMaxElevation.toString(),
            "algorithm": algorithm.toString(),
            "path_limit": pathLimit
        }

        submitData = JSON.stringify(submitData);

        $.ajax({
            type: "POST",
            url: "/path_via_address",
            data: submitData,
            success: function(data) {
                plotRoute(data, "address")
                updateOutputs(data)
            },
            dataType: "json"
        });
    }

};

function plotRoute(data, endpoint) {
    console.log(data)
    if (data["bool_pop"] === -1) {
        if (originMarker) {
            originMarker.remove();
        }
        if (destMarker) {
            destMarker.remove();
        }
        resetOutputs();
        return;
    }

    if(data["bool_pop"]==0 || data["bool_pop"]===1) {
        return;
    }

    map.addSource("ele_route", {
        "type": "geojson",
        "data": data["elev_path_route"]
    });

    map.addLayer({
        "id": "ele_route",
        "type": "line",
        "source": "ele_route",
        "layout": {
            "line-join": "round",
            "line-cap": "round"
        },
        "paint": {
            "line-color": "Blue",
            "line-width": 5
        }
    });

    map.addSource("shortest_route", {
        "type": "geojson",
        "data": data["shortest_route"]
    });

    map.addLayer({
        "id": "shortest_route",
        "type": "line",
        "source": "shortest_route",
        "layout": {
            "line-join": "round",
            "line-cap": "round"
        },
        "paint": {
            "line-color": "Red",
            "line-width": 2
        }
    });

    updateOutputs(data);
}

function updateOutputs(data) {
    document.getElementById("shortestDistance").innerHTML = data["shortDist"].toFixed(4) + "meters";
    document.getElementById("elevationDistance").innerHTML = data["elev_path_dist"].toFixed(4) + "meters";
    document.getElementById("gainShort").innerHTML = data["gainShort"].toFixed(4) + "meters";
    document.getElementById("dropShort").innerHTML = data["dropShort"].toFixed(4) + "meters";
    document.getElementById("elev_path_gain").innerHTML = data["elev_path_gain"].toFixed(4) + "meters";
    document.getElementById("elev_path_drop").innerHTML = data["elev_path_drop"].toFixed(4) + "meters";
}

mapboxgl.accessToken = access_key;
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v10',
    center: [-72.529262, 42.384803],
    zoom: 13,
});


var originMarker, destMarker;
points = turf.featureCollection([]);

map.on("load" , function(){
    map.addSource('circleData', {
        type: 'geojson',
        data: {
        type: 'FeatureCollection',
        features: [],
        },
    });
    map.addLayer({
        id: 'data',
        type: 'circle',
        source: 'circleData',
        paint: {
        'circle-opacity' : 0.1,
        'circle-radius': 300,
        'circle-stroke-width': 2,
        'circle-stroke-color': '#333',
        },
    });
});

map.on('mousemove', function (e) {
    document.getElementById('latitude').innerHTML = e.lngLat["lat"].toFixed(4);
    document.getElementById('longitude').innerHTML = e.lngLat["lng"].toFixed(4);
});

map.on('click', function(e){
    if(isSelect) {
        lngLat = new Array(e.lngLat.lng, e.lngLat.lat);
        if(!setOriginFlag) {
            originMarker = setMapMarker('origin', e);
            originCoords = JSON.stringify(e.lngLat);
            setOriginFlag = true;
            map.flyTo({center: lngLat});
        } else if (!setDestFlag){
            destMarker = setMapMarker('dest', e);
            destCoords = JSON.stringify(e.lngLat);
            setDestFlag = true;
            map.flyTo({center: lngLat});
        }

    }
});