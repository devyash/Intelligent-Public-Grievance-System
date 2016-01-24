var mapOptions = {
    center: new google.maps.LatLng(37.7831,-122.4039),
    zoom: 10,
    mapTypeId: google.maps.MapTypeId.ROADMAP
};

new google.maps.Map(document.getElementById('map'), mapOptions);