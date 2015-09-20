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

this.options.drawMarkers= function(position,msg) {
  var marker, myLatLng;
  myLatLng = {};
  myLatLng.lat = position.lat;
  myLatLng.lng = position.lng;
  return marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    title: msg
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
    var postdata = {}
    postdata.start = this.startCoords.lat+","+this.startCoords.lng
    postdata.end = this.endCoords.lat+","+this.endCoords.lng
    $.ajax({
      url: "http://bigredtransit.co/route",
      type: "POST",
      data:postdata,
      dataType: "json"
    }).done(function(res) {
      window.options.parseData(res);
      $('div.loading').hide();
      $('div#homepage').animate({top:"-100%"},"slow").hide()
      return $('div#searchresult').animate({top:"0"},"slow").show()
    });
    return true;
  }
};


/*
Parse data for using in drawing the route
 */

this.options.parseData = function(data) {
  var alldata = JSON.parse(data);
  if(alldata.length == 0){return alert("No results found, please try another search!")}
  var templateHTML = "<div class='cards' data-index='__DATA_INDEX__' data-startCoords='__STARTCOORDS__' data-endCoords='__ENDCOORDS__'><span class='left'></span><div class='info'><h3>__ROUTE_NUMBER__</h3><span class='time'>__ROUTE_TIME__</span><span class='direction'>__ROUTE_DIRECTION__</span></div><span class='icon'></span><span class='right'></span></div>"
  var renderHTML = ''
  for(i in alldata){
    for(j in alldata[i]['Routes']){
      renderHTML += templateHTML.replace('__ROUTE_NUMBER__',alldata[i]['Routes'][j]).replace('__ROUTE_TIME__',alldata[i]['Time'][j]).replace('__ROUTE_DIRECTION__',alldata[i]['Direction']).replace('__STARTCOORDS__',this.startCoords.lat+","+this.startCoords.lng).replace('__ENDCOORDS__',this.endCoords.lat+","+this.endCoords.lng).replace('__DATA_INDEX__',j)
    }
  }
  $('div#result_cards').html(renderHTML);
  showMapData(0);
};

showMapData = function(ind){

  var ele = $('div.cards').eq(ind);
  var position = {}
  var start = ele.attr("data-startCoords")
  position.lat = start.split(",")[0]
  position.lng = start.split(",")[1]
  window.options.drawMarkers(position,"From")
  var end = ele.attr("data-endCoords")
  position.lat = end.split(",")[0]
  position.lng = end.split(",")[1]
  window.options.drawMarkers(position,"To")
}

$('#gosearch').on('click', function(e) {
  window.options.search()
});

$('#backtohome').on('click', function(e) {
  e.preventDefault();
  e.stopPropagation();
  $('div#homepage').animate({top:"0"},"slow").show();
  $('div#searchresult').animate({top:"100%"},"slow").hide();
})

$('#searchresult').on("click","span.left",function(){
  var ele = $(this).closest("div.cards");
  if(ele.attr("data-index")=="0"){
    return alert("Already the first one!")
  }
  ele.prev("div.cards").show();
  showMapData(ele.attr("data-index"));
});

$('#searchresult').on("click","span.right",function(){
  var ele = $(this).closest("div.cards");
  if(!ele.next('div.cards')){
    return alert("No more options!")
  }
  ele.hide();
  showMapData(ele.attr("data-index"));
})
