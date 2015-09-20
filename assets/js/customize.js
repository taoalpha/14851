var coords;

this.options = {};

this.options.map;

this.options.currentCoords = {};

this.options.startLocation;

this.options.startCoords = {};

this.options.endLocation;

this.options.endCoords = {};

this.options.drawCoords = {};

coords = [
  {
    lat: 42.456261,
    lng: -76.471623
  }, {
    lat: 42.447484,
    lng: -76.482116
  }, {
    lat: 42.447467,
    lng: -76.467641
  }, {
    lat: 42.4612,
    lng: -76.49985
  }, {
    lat: 42.43985,
    lng: -76.499133
  }
];


/*
Draw the route according to the coords we have for this route
 */

this.options.drawTheMap = function(coords) {
  var drawThePath;
  this.map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: {
      lat: 42.4412,
      lng: -76.48985
    },
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });
  drawThePath = new google.maps.Polyline({
    path: coords,
    geodesic: true,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2
  });
  return drawThePath.setMap(this.map);
};


/*
Add autocomplete for two input
 */

this.options.initAutocomplete = function() {
  this.startLocation = new google.maps.places.Autocomplete(document.getElementById('start'), {
    types: ['geocode']
  });
  this.endLocation = new google.maps.places.Autocomplete(document.getElementById('destination'), {
    types: ['geocode']
  });
  this.startLocation.addListener('place_changed', this.getStart);
  return this.endLocation.addListener('place_changed', this.getEnd);
};


/*
Get coords of start location
 */

this.options.getStart = function() {
  var place;
  place = this.startLocation.getPlace();
  this.startCoords.lat = place.geometry.location.H;
  return this.startCoords.lng = place.geometry.location.L;
};


/*
Get coords of end location
 */

this.options.getEnd = function() {
  var place;
  place = this.endLocation.getPlace();
  this.endCoords.lat = place.geometry.location.H;
  return this.endCoords.lng = place.geometry.location.L;
};

this.options.getLocation = function() {
  if (navigator.geolocation) {
    return navigator.geolocation.getCurrentPosition(this.updatePos, this.showError);
  } else {
    return alert("Geolocation is not supported by this browser.");
  }
};

this.options.updatePos = function(position) {
  var marker, myLatLng;
  myLatLng = {};
  myLatLng.lat = position.coords.latitude;
  myLatLng.lng = position.coords.longitude;
  return marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    title: 'Here you are!'
  });
};

this.options.showError = function(e) {
  switch (e.code) {
    case e.PERMISSION_DENIED:
      console.log("You denied the request for Geolocation.");
      return this.currentCoords = 1;
    case e.POSITION_UNAVAILABLE:
      console.log("Location information is unavailable.");
      return this.currentCoords = 0;
    case e.TIMEOUT:
      console.log("The request to get user location timed out.");
      return this.currentCoords = 0;
    case e.UNKNOWN_ERROR:
      console.log("Unknow error");
      return this.currentCoords = 0;
  }
};


/*
Main function for the callback of google maps api
 */

this.options.main = function() {
  this.initAutocomplete();
  return this.getLocation();
};

this.options.search = function() {

  /*
  logic: currentCoords == 0 -> tip: fail to get the location, need input the location
  logic: currentCoords == 1 -> tip: you should allow us to access your geo data if you want to use your location.
   */
  if (this.currentCoords === 0) {
    this.showErrorTip("Sorry, fail to get the location, need input the location.");
    return false;
  } else if (this.currentCoords === 1) {
    this.showErrorTip("You should allow us to access your geo data if you want to use your location.");
    return false;
  } else {
    $('div.loading').show();
    $.ajax({
      url: "",
      type: "GET",
      dataType: "json"
    }).done(function(res) {
      window.options.parseData(res);
      $('div.loading').hide();
      $('div#homepage').animate({top:"-100%"},"slow")
      return $('div#searchresult').animate({top:"0"},"slow")
    });
    return true;
  }
};


/*
Parse data for using in drawing the route
 */

this.options.parseData = function(data) {
  return this.drawCoords = JSON.parse(data);
};

$('#gosearch').on('click', function(e) {
  if (!window.options.search) {

  }
});

$('#backtohome').on('click', function(e) {
  e.preventDefault();
  e.stopPropagation();
  $('div#homepage').animate({top:"0"},"2000");
  $('div#searchresult').animate({top:"100%"},"3000").hide();
})
