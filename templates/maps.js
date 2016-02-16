var markersArray = [];
function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 14,
    center: {lat: 19.1987603, lng: 72.872997 }
  });

  map.addListener('click', function(e) {
    placeMarkerAndPanTo(e.latLng, map);
  });
}

function placeMarkerAndPanTo(latLng, map) {
  var position = latLng;
  while (markersArray.length) {
    markersArray.pop().setMap(null);
  }
  var marker = new google.maps.Marker({
    position: latLng,
    map: map,
    draggable:true
  });
  map.panTo(latLng);
  markersArray.push(marker);
  var lat = marker.getPosition().lat();
  var lng = marker.getPosition().lng();
  document.getElementById("lat").innerHTML = lat;
  document.getElementById("lng").innerHTML = lng;

}

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      document.getElementById("lat").innerHTML = pos.lat;
      document.getElementById("lng").innerHTML = pos.lng;
    });


  }

//different color markers
//marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png')
//marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png')
//marker.setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png')