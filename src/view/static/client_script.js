function setVisibilityOfAddressTexts(disabled){
  document.getElementById("text_start_address").disabled = disabled;
  document.getElementById("text_end_address").disabled = disabled;
};


function roundOff(N){
  return Math.round(N*10000)/10000;
}

function updateEndPointLocations(position){
  var color = '';
  if(position === 'start') color = 'red';
  else color = 'blue';

  document.getElementById(position).innerHTML ="Start Location:("+roundOff(e.lngLat["lat"])+","+roundOff(e.lngLat["lng"])+")";

  var m = new mapboxgl.Marker({color:color})
  .setLngLat(e.lngLat)
  .addTo(map);

  return m;
}
