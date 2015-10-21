////////////////////////
// VARIABLES GLOBALES //
////////////////////////

var map;
var markers = []; // [google_object]
var selected_marker_id = -1;
var selected_marker = null;
var markers_search = [];
var searchBox;
var scoreboard_is_hidden = false;
var pointer_marker = null;
var panorama;

///////////////////////
// FUNCIONES DE LM //
///////////////////////
function mostrar(){
        
        if ( panorama.getVisible() == false) {
            //no se muestra
            document.getElementById('mapbutton').style= 'display: none';//firefox
            document.getElementById('mapbutton').style.display='none'; //chrome
            document.getElementById('mapbutton').style = 'visibility: hidden';
            document.getElementById('mapbutton').style.visibility  = 'hidden'; 
               
        } else {
            //se muestra el button
            document.getElementById('mapbutton').style= 'display: \'\'';
            document.getElementById('mapbutton').style.display='';
            document.getElementById('mapbutton').style = 'visibility: visible';
            document.getElementById('mapbutton').style.visibility  = 'visible';
        }
    }

///////////////////////
// FUNCIONES DE CSRF //
///////////////////////


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
                }
            }
        }
    return cookieValue;
    }
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }



///////////////////
// MAP FUNCTIONS //
///////////////////
function set_marker_status(marker, new_status){

    var new_icon = {
        url: '/static/project/images/status_' + new_status + '.svg',
        scaledSize: new google.maps.Size(24, 24),
        anchor: new google.maps.Point(12, 12),
    };
    marker.setIcon( new_icon );
    marker.local_custom_status = new_status;
    change_color_div_status(new_status);
}

function set_marker_hitscore_label(marker, hitscore_value){
    marker.set('labelAnchor', new google.maps.Point(9, 24) );
    marker.set('labelContent', hitscore_value);
}

function load_score_board(){
    var select_project = document.getElementById('select_project');
    var iframe_score_board = document.getElementById('iframe_score_board');
    var project_id = select_project.value;
    var score_board_url = "/map/score_board";
    update_location_summary_model_message()
    iframe_score_board.src = score_board_url + "?project_id=" + project_id;
}

function get_score_board_heigth(){
    var iframe_score_board = document.getElementById('iframe_score_board');
    var number_of_rows = iframe_score_board.contentWindow.get_scoreboard_rows();
    var scoreboard_height = (number_of_rows * 15) + 30;
    return scoreboard_height;
}

function score_board_loaded(){
    var div_score_board = document.getElementById('div_score_board');
    var iframe_score_board = document.getElementById('iframe_score_board');
    div_score_board.style.height= get_score_board_heigth() + 'px';
    iframe_score_board.style.opacity = "1";
    scoreboard_is_hidden = false;
}

function show_hide_scoreboard(){
    var div_score_board = document.getElementById('div_score_board');
    var iframe_score_board = document.getElementById('iframe_score_board');
    if (scoreboard_is_hidden){
        div_score_board.style.height= get_score_board_heigth() + 'px';
        iframe_score_board.style.opacity = "1";
        }
    else {
        div_score_board.style.height = '24px'
        iframe_score_board.style.opacity = "0";
        }
    scoreboard_is_hidden = ! scoreboard_is_hidden;
    }

function clear_map() {
    for (i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
    if (pointer_marker != null){    //remove pointer
        pointer_marker.setMap(null);
    }
  }

function plot_points() {
    var csrftoken = getCookie('csrftoken');
    $("#notification_div")[0].innerHTML= '';
    $("#notification_div").css("background-color", "");

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

    clear_map();
    $.ajax({
        url:'/project/get_points',
        type: "POST",
        data: {'p_proj_id': parseInt(document.getElementById('select_project').value)},
        success:function(response){
            points = response['points'];
            var bounds = new google.maps.LatLngBounds();
            var con = 0;
            var status6 = 0;
            for (i = 0; i < points.length; i++) {
                var pos = new google.maps.LatLng(points[i][0],points[i][1]);
                var marker = new MarkerWithLabel({
                    position: pos,
                    map: map,
                    labelClass: 'marker_label'
                    });
                marker.local_custom_point_id = points[i][2];
                marker.local_custom_status = points[i][3];
                marker.local_custom_hitscore = points[i][4];
                set_marker_status(marker,points[i][3]);
                if (points[i][3] == 6) {status6 = status6+1;}
                if( points[i][4] != null){
                    set_marker_hitscore_label(marker, points[i][4]);
                    }
                markers.push(marker)
                add_listener_to_marker(marker);
                bounds.extend(marker.position);
                con = con + 1;
                }
            if (con == 0) {
                map.setCenter(new google.maps.LatLng(41.92,12.51));
                map.setZoom(2);
                }
            else if(con == 1){
                map.setCenter(bounds.getCenter());
                map.setZoom(5);
                }
            else{
                map.fitBounds(bounds);
                }
            if (status6 > 0) {
                string = ' ';
                string = string.concat(status6.toString());
                string = string.concat(' ')
                $("#notification_div")[0].innerHTML= string;
                $("#notification_div").css("background-color", "red");
                }

            document.getElementById("input_location_name").value = "";
            document.getElementById("location_summary_hitscore_hitscore").innerHTML = "no hitscore computed for this location";
            selected_marker_id = -1;
            selected_marker = null;
            },
        complete:function(){},
        error:function (xhr, textStatus, thrownError){}
        });
    }


function initialize() {
    //INIT MAP
    // estilos del mapa
    var styles = [
        {
        "featureType": "poi",
        "elementType": "all",
        "stylers": [
            { "visibility": "off" }
            ]
        },
        {
        "featureType": "landscape",
        "elementType": "labels.text",
        "stylers": [
            {"color": "#ffffff"},
            {"weight": 1}
            ]
        },
        {
        "featureType": "landscape",
        "elementType": "labels.icon",
        "stylers": [
            { "visibility": "off" }
            ]
        },
        {
        "featureType": "transit",
        "elementType": "labels.icon",
        "stylers": [
            { "visibility": "off" }
            ]
        },
        {
        "featureType": "transit.line",
        "elementType": "all",
        "stylers": [
            {"hue": "#000000"},
            {"visibility": "on"},
            {"weight":1}
            ]
        },
        {
        "featureType": "road",
        "elementType": "labels.icon",
        "stylers": [
            { "visibility": "off" }
            ]
        },
        {
        "featureType": "road.highway",
        "elementType": "labels",
        "stylers": [
            { "visibility": "on" }
            ]
        },
        {
        "featureType": "road.highway",
        "elementType": "labels.icon",
        "stylers": [
            { "visibility": "off" }
            ]
        },
        {
        "featureType": "road.highway",
        "elementType": "geometry",
        "stylers": [
            { "visibility": "on" },
            { "color": "#ffffff" }
            ]
        },
        {
        "featureType": "water",
        "elementType": "geometry.fill",
        "stylers": [
            {"color": "#B2B2B2"}
            ]
        },
        {
        "featureType": "water",
        "elementType": "labels.text",
        "stylers": [
            {"color": "#ffffff"},
            {"weight": 1}
            ]
        }
    ];

    var mapOptions = {
        center: { lat: 17.418, lng: -68.178456},
        zoom: 3,
        styles: styles,
          mapTypeControlOptions: {
          style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
          position: google.maps.ControlPosition.LEFT_TOP
        },
	overviewMapControl:true,
	panControl:false,
	zoomControl:true,
	zoomControlOptions: {
          style:google.maps.ZoomControlStyle.SMALL,
	  position: google.maps.ControlPosition.LEFT_TOP
        },
    };

    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    panorama = map.getStreetView();
    mostrar();  //oculta  el boton al inicar
    
    //POINT EVENT
    google.maps.event.addListener(map, 'click', function(event) {
        placeMarker(event.latLng); 
        });

       plot_points();

       var input = /** @type {HTMLInputElement} */(
       document.getElementById('pac-input'));
       map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

       searchBox = new google.maps.places.SearchBox(
       /** @type {HTMLInputElement} */(input));

      google.maps.event.addListener(searchBox, 'places_changed', function() {
      var places = searchBox.getPlaces();

      if (places.length == 0) {
        return;
      }
      
     for (var i = 0, marker; marker = markers_search[i]; i++) { //REVISAR POR QUE ESTA ACA
       marker.setMap(null);
     }

    markers_search = [];
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0, place; place = places[i]; i++) {
      var image = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };

      // Create a marker for each place.
      var marker = new MarkerWithLabel({
        map: map,
        icon: image,
        title: place.name,
        position: place.geometry.location,
        labelClass: 'marker_label'
      });

      markers_search.push(marker);
      map.setCenter(place.geometry.location);
      map.setZoom(15);
    }

  });  // fin search_box event

  google.maps.event.addListener(map, 'bounds_changed', function() {
    var bounds = map.getBounds();
    searchBox.setBounds(bounds);
    mostrar();  //oculta  el boton al inicar
  });
  
  //load score board
  load_score_board();
}


function toggleStreetView() {
    var toggle = panorama.getVisible();
 
    if (toggle == false) {
       mostrar();  //oculta el boton al salir de la panormica
    } else {               
       panorama.setVisible(false);   
       mostrar();  //oculta el boton al salir de la panormica    
    }
    
}

//POINT FUNCTION
function placeMarker(location) {
    marker = new MarkerWithLabel({
        position: location,
        map: map,
        labelClass: 'marker_label'
        });
    $.when(save_new_point(location)).done(function(response){
        marker.local_custom_point_id = selected_marker_id;
        marker.local_custom_status = response.status;
        selected_marker = marker;
        set_marker_status(marker, response.status);
        markers.push(marker)
        add_listener_to_marker(marker);
        load_score_board();
        click_marker(marker);
        reload_location_summary_sales(selected_marker.local_custom_point_id);
        reload_location_summary_hitscore(selected_marker.local_custom_point_id);
        reload_location_summary_status(selected_marker.local_custom_status);
        change_color_div_status(selected_marker.local_custom_status);
        });
    }

function save_new_point(location) {
    //send the lat and lon of a new point to the server
    //the server save the new point and return the new point_id
    //update selected_marker_id with new point_id
    var csrftoken = getCookie('csrftoken');
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

    return $.ajax({
        url:'/project/add_point',
        type: "POST",
        data: {lat: location.lat(), lon:location.lng(), project:parseInt(document.getElementById('select_project').value)},
        success:function(response){
            ok = response.response;
            selected_marker_id = response['id'];
        },
            error:function (xhr, textStatus, thrownError){}
        });
    }



function add_project(){
    var select_project = document.getElementById('select_project');
    var new_option = document.createElement("Option");
    var new_project_name = prompt('Enter the new project\'s name', 'project name');
    var new_project_id;
    var csrftoken = getCookie('csrftoken');
    //validate new_project_name
    if (new_project_name == null){
        return;
        }
    else {
        new_project_name = new_project_name.trim();
        if (new_project_name == ""){
            return;
        }
    }

    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

    $.ajax({
    url:'/project/create_project',
    type: "POST",
    data: {'new_project': new_project_name},
    success:function(response){
        new_project_id = parseInt(response['project_id']);
        //check if a project with that name already exists.
        if(new_project_id > 0){
            new_option.text = new_project_name;
            new_option.value = new_project_id;
            select_project.add(new_option);
            select_project.value = new_option.value;
            clear_map();
            load_score_board();
            map.setCenter(new google.maps.LatLng(41.92,12.51));
            map.setZoom(2);
            document.getElementById("input_location_name").value = "";
            document.getElementById("location_summary_hitscore_hitscore").innerHTML = "no hitscore computed for this location";
            selected_marker_id = -1;
            selected_marker = null;
            }
        else {
            //there is a project with given name. No new project were created. Alert to user.
            alert('A project called "' + new_project_name + '" already exists.');
            }
        },
        complete:function(){},
        error:function (xhr, textStatus, thrownError){}
        });
    }

function add_listener_to_marker(marker){
    google.maps.event.addListener(marker, 'click', function (){
          click_marker(marker)
        });
    }

function click_marker(marker){
    selected_marker_id = -1;
    selected_marker = null; 
    clicked_point_id = marker.local_custom_point_id; // id del punto
    selected_marker_id = clicked_point_id;
    selected_marker = marker;  // marker
    
    reload_location_summary_sales(clicked_point_id);
    reload_location_summary_hitscore(clicked_point_id);
    reload_location_summary_status(clicked_point_id);
    set_pointer_marker(marker);
    set_selected_marker_scoreboard(clicked_point_id);
    
}

function set_selected_marker_scoreboard(point_id){
    var win_score_board = document.getElementById('iframe_score_board').contentWindow;  
    win_score_board.set_tr_selected(point_id);
}

function set_pointer_marker(marker){
    var location = marker.getPosition();
    var pointer_icon = {
        url: '/static/project/images/selected.svg',
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(18, 18),
        scaledSize: new google.maps.Size(36, 36)
        };
    if (pointer_marker != null){
        //remove previous pointer
        pointer_marker.setMap(null);
        }
    pointer_marker = new google.maps.Marker({
        position: location,
        map: map,
        icon: pointer_icon
        });
    }

google.maps.event.addDomListener(window, 'load', initialize);

function show_point_data(marker_id){
    var marker_sales;
    var span_marker_id = document.getElementById('span_marker_id');
    var input_sales = document.getElementById('input_sales');
    var hidden_marker_id = document.getElementById('hidden_marker_id');
    var span_update_sale = document.getElementById('span_update_sales');
    var button_update_sale = document.getElementById('button_update_sales');
    var span_hitscore = document.getElementById('span_hitscore');
    var button_compute_hitscore = document.getElementById('button_compute_hitscore');
    var new_span_text_node;
    var hitscore;
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

    $.ajax({
        url:'/project/get_point_data',
        type: "POST",
        data: {'point_id': marker_id},
        success:function(response){
            //write point id
            new_span_text_node = document.createTextNode(marker_id);
            span_marker_id.innerText = new_span_text_node.textContent;
            span_marker_id.textContent = new_span_text_node.textContent;
            hidden_marker_id.value = marker_id;
            //write point sales
            if ('sales' in response){
                marker_sales = response['sales'];
                }
            else {
                marker_sales = "";
                }
            input_sales.value = marker_sales;
            //write hitscore
            if ('hitscore' in response){
                hitscore = response['hitscore'];
                button_compute_hitscore.style = 'visibility: hidden'; //firefox
                button_compute_hitscore.style.visibility = 'hidden';  //chorme
                }
            else {
                hitscore = "";
                button_compute_hitscore.style = 'visibility: visible';
                button_compute_hitscore.style.visibility = 'visible';
                }
            new_span_text_node = document.createTextNode(hitscore);
            span_hitscore.innerText = new_span_text_node.textContent;
            span_hitscore.textContent = new_span_text_node.textContent;
            //write other messages
            span_update_sales.innerText = ""
            span_update_sales.textContent = ""
            button_update_sales.disabled = false;
            },
        complete:function(){},
        error:function (xhr, textStatus, thrownError){}
        });
    }



function change_point_status(){
    var marker_id = selected_marker_id;
    var marker = selected_marker;
    var select_status = document.getElementById('select_status');
    var status  = select_status.value;
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});
    
   $.ajax({
        url:'/project/change_point_status/',
        type: "POST",
        data: {'marker_id': marker_id, 'status': status},
        success:function(response){
            if (response['response'] == 'OK'){
                load_score_board();
                set_marker_status(marker, status);
                }
            else if (response['response'] == 'error' ){
                alert('Error.\n' + response['error_message']);
                }
            },
        complete:function(){},
        error:function (xhr, textStatus, thrownError){}
        });
    }


function center_map(point_id){
    var latLng;
    var n_markers = markers.length;
    var i;
    var found = false;
    for (i = 0 ; i < n_markers ; i++){
        if (markers[i].local_custom_point_id == point_id){
            found = true;
            break;
            }
        }
    if (found){
        click_marker(markers[i]);
        latLng = markers[i].getPosition();
        map.setCenter(latLng);
        map.setZoom(18);
        }
    }

function Report(){
    var proje = document.getElementById("select_project").value;
    var fecha = new Date();
    var date = fecha.getDate() + "/" + (fecha.getMonth() + 1) + "/" + fecha.getFullYear()

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});
    $.ajax({
        url:'/map/Reporte_Location_Summary',
        type: "POST",
        data: {'proyecto': proje, 'fecha': date},
        success:function(response){
            console.log(response.Response);
            },
        complete:function(){},
        error:function (xhr, textStatus, thrownError){}
        });
    }

function reporte_scoreboard(){
    var proje = document.getElementById("select_project").value;
    var fecha = new Date();
    var date = fecha.getDate() + "/" + (fecha.getMonth() + 1) + "/" + fecha.getFullYear()

    var csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});
   $.ajax({
        url:'/map/Reporte_Scoreboard',
        type: "POST",
        data: {'proyecto': proje, 'fecha': date},
        success:function(response){
            console.log(response.Response);
            },
        complete:function(){},
        error:function (xhr, textStatus, thrownError){}
        });
    }

function edit_project(){
    var select_project = document.getElementById('select_project');
    var selected_project = select_project.value;
    location.href = '/project/' + selected_project;
    }

function delete_project(){
    var confirmed  = false;
    var select_project = document.getElementById('select_project');
    var selected_project = select_project.value;
    var csrftoken = getCookie('csrftoken');
    confirmed = confirm("Do you want to delete this project?");
    if (!confirmed){
        return;
        }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});
        $.ajax({
            url:'/project/delete_project/',
            type: "POST",
            data: {
               'project_id': selected_project
                },
        success:function(response){
            if (response['response'] == 'OK'){
                select_project.remove(select_project.selectedIndex);
                select_project.value = select_project.options[0].value;
                plot_points();
                load_score_board();
                alert("Project has been deleted.");
                } else {
                alert("Error\n" + response['error_message']);
                }
            },
        complete:function(){},
        error:function (xhr, textStatus, thrownError){}
        });
    }


function call_logout(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

        $.ajax({
            url:'/login/signout/',
            type: "POST",
            data: {},
        success:function(response){
            if (response['status'] == 'OK'){
                window.location = "/";
                }
            },
        complete:function(){},
        error:function (xhr, textStatus, thrownError){}
        });
    }

