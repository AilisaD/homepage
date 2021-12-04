let map = L.map('map', { zoomControl: false }).setView([55.81370, 37.36522], 6);
let gl = L.mapboxGL({
    style: 'https://api.maptiler.com/maps/35d9173d-5587-4156-a635-57776a4c15f6/style.json?key=auHeH62VVMXfIVFOMESZ',
    zoomControl: false
}).addTo(map);

let timestamps = [];
let radarLayers = [];
let animationPosition = 0;
let removeZeroLayer = 0;

function getNewTime(){
    let f = true;
    if(timestamps.length === 0){
        f = false;
    }
    else{
        removeZeroLayer = timestamps[0];
    }
    let apiRequest = new XMLHttpRequest();
    apiRequest.open("GET", "https://api.rainviewer.com/public/maps.json", f);
    apiRequest.onload = function(e) {
        timestamps = JSON.parse(apiRequest.response);
    };
    apiRequest.send();
    setTimeout(getNewTime, 1000*60*10);

}
getNewTime();


if (timestamps.length !== 0)
{
    play();
}


function addLayer(ts) {
    if (removeZeroLayer !== 0){
        map.removeLayer(radarLayers[removeZeroLayer]);
    }
    if (!radarLayers[ts]) {
        let layers = 'https://tilecache.rainviewer.com/v2/radar/' + ts + '/256/{z}/{x}/{y}/8/1_1.png';
        radarLayers[ts] = new L.TileLayer(layers, {
            tileSize: 256,
            opacity: 0.001,
            zIndex: ts
        });
    }
    if (!map.hasLayer(radarLayers[ts])) {
        map.addLayer(radarLayers[ts]);
    }
}

function changeRadarPosition(position, preloadOnly) {
    while (position >= timestamps.length) {
        position -= timestamps.length;
    }
    while (position < 0) {
        position += timestamps.length;
    }

    let currentTimestamp = timestamps[animationPosition];
    let nextTimestamp = timestamps[position];

    addLayer(nextTimestamp);

    if (preloadOnly) {
        return;
    }
    animationPosition = position;

    if (radarLayers[currentTimestamp]) {
        radarLayers[currentTimestamp].setOpacity(0);
    }
    radarLayers[nextTimestamp].setOpacity(100);
}

function showFrame(nextPosition) {
    let preloadingDirection = nextPosition - animationPosition > 0 ? 1 : -1;
    changeRadarPosition(nextPosition);
    changeRadarPosition(nextPosition + preloadingDirection, true);
}

function play() {
    showFrame(animationPosition + 1);
    let timeout = 500;
    if (animationPosition === timestamps.length-1)
    {
        timeout += 4500;
    }
    move();
    setTimeout(play, timeout);
}

var i = 0;
function move() {
    if (i === 0) {
        i = 1;
        let elem = document.getElementById("load");
        let width = 1;
        let id = setInterval(frame, 63.8);
        function frame() {
            if (width >= 100) {
                clearInterval(id);
                i = 0;
            } else {
                width++;
                elem.style.width = width + "%";
            }
        }
    }
}





