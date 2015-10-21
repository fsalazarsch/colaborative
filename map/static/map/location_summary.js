
function change_color_div_status( new_status ){
    var color_confirm_data = "rgba(137,39,167,0.7)";
    var color_in_negotiation = 'rgba(49,180,4,0.7)';
    var color_rejected = 'rgba(132,132,132,0.7)';
    var color_other_status = '#004050';
    var color_open = 'rgba(46,46,46,0.7)';
    var color_interested = 'rgba(56,155,210,0.7)';
    var div_status = document.getElementById('div_status');
    var accordian =  document.getElementById('accordian');
    switch (new_status){
        case '1':
        case 1:
            div_status.style.backgroundColor = color_interested;
            accordian.style.backgroundColor = color_interested;
            div_status.style = 'background-color: ' + color_interested;
            accordian.style = 'background-color: ' + color_interested;
            break;
        case '2':
        case 2:
            div_status.style.backgroundColor = color_confirm_data;
            accordian.style.backgroundColor = color_confirm_data;
            div_status.style = 'background-color: ' + color_confirm_data;
            accordian.style = 'background-color: ' + color_confirm_data;
            break;
        case '3':
        case 3:
            div_status.style.backgroundColor = color_in_negotiation;
             accordian.style.backgroundColor = color_in_negotiation;
            div_status.style = 'background-color: ' + color_in_negotiation;
            accordian.style = 'background-color: ' + color_in_negotiation;
            break;
        case '4':
        case 4:
            div_status.style.backgroundColor = color_rejected;
            accordian.style.backgroundColor = color_rejected;
            div_status.style = 'background-color: ' + color_rejected;
            accordian.style = 'background-color: ' + color_rejected;
            break;
        case '5':
        case 5:
            div_status.style.backgroundColor = color_open;
            accordian.style.backgroundColor = color_open;
            div_status.style = 'background-color: ' + color_open;
            accordian.style = 'background-color: ' + color_open;
            break;
        default:
            div_status.style.backgroundColor = color_other_status;
            accordian.style.backgroundColor = color_other_status;
            div_status.style = 'background-color: ' + color_other_status;
            accordian.style = 'background-color: ' + color_other_status;
    }
}




function get_point_info(id_point){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

 $.ajax({
        url:'/project/get_points_information',
        type: "POST",
        data: {'id_point':id_point},
        success:function(response){
            point_info = response.point_information;
            console.log(point_info);
        },
        complete:function(){},
            error:function (xhr, textStatus, thrownError){}
        });
    }




function compute_hitscore(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

    if (selected_marker_id > 0) {
        var select_project = document.getElementById('select_project');
        var project_id = select_project.value;

        $.ajax({
            url:'/project/predict_hitscore',
            type: "POST",
            data: {'point_id':selected_marker_id},
            success:function(response){
                if ('hitscore' in response){
                    reload_location_summary_hitscore(selected_marker_id);
                    }
                else {
                    var label_location_summary_hitscore_hitscore = document.getElementById('location_summary_hitscore_hitscore');
                    label_location_summary_hitscore_hitscore.innerHTML = 'no hitscore computed for this location';
                    alert("Please, upload your data (sales) and then click on 'I am ready to make a prediction model'");
                    }
                },
            error:function (xhr, textStatus, thrownError){}
            });
        }
    else {
        alert("unselected point");
        }
    }

function reload_location_summary_hitscore(point_id){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

    var label_location_summary_hitscore_hitscore = document.getElementById('location_summary_hitscore_hitscore');

    $.ajax({
        url:'/project/get_hitscore',
        type: "POST",
        data: {'point_id': point_id},
        success:function(response){
            if ('hitscore' in response){
                var parsed_hitscore = parseInt(response['hitscore'],10)
                label_location_summary_hitscore_hitscore.innerHTML = parsed_hitscore;
                set_marker_hitscore_label(selected_marker, parsed_hitscore);
                }
            else {
                label_location_summary_hitscore_hitscore.innerHTML = 'no hitscore computed for this location';
                }
        },
        error:function (xhr, textStatus, thrownError){}
        });
    }




function update_location_summary_point_sales(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

    var input_yearly_sales = document.getElementById('location_summary_sales_yearly_sales').value;
    var input_date_opening = document.getElementById('location_summary_sales_date_opening').value;
    var input_days_opened = document.getElementById('location_summary_sales_days_opened').value;
    var input_square_feet = document.getElementById('location_summary_sales_square_feet').value;
    var element_done_span = document.getElementById('location_summary_sales_done_span');

    if (selected_marker_id > 0) {
        $.ajax({
            url:'/project/update_point_sales',
            type: "POST",
            data: { 'point_id':selected_marker_id,
                    'yearly_sales':input_yearly_sales, 
                    'date_opening':input_date_opening,
                    'days_opened':input_days_opened, 
                    'square_feet':input_square_feet },
            success:function(response){
                element_done_span.innerText = response['msg'];
                load_score_board();
                },
            error:function (xhr, textStatus, thrownError){}
            });
        }
    else {
        alert("unselected point");
        }
    }


function update_location_summary_point_notes(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

    var input_notes_owner = document.getElementById('notes_owner').value;
    var input_notes_contact = document.getElementById('notes_contact').value;
    var input_notes_address = document.getElementById('notes_address').value;
    var input_notes_price = document.getElementById('notes_price').value;
    var input_notes_area = document.getElementById('notes_area').value;
    var input_notes_tip_price = document.getElementById('notes_tip_price').value;
    var input_notes_tip_area = document.getElementById('notes_tip_area').value;
    var element_done_span2 = document.getElementById('location_summary_notes_done_span');

    if (selected_marker_id > 0) {
        $.ajax({
            url:'/project/update_point_notes',
            type: "POST",
            data: { 'point_id':selected_marker_id,
                    'notes_owner':input_notes_owner,
                    'notes_contact':input_notes_contact,
                    'notes_address':input_notes_address,
                    'notes_price':input_notes_price,
                    'notes_area':input_notes_area,
                    'notes_tip_area':input_notes_tip_area,
                    'notes_tip_price':input_notes_tip_price},
            success:function(response){
                element_done_span2.innerText = response['msg'];
                },
            error:function (xhr, textStatus, thrownError){}
            });
        }
    else {
        alert("unselected point");
        }
    }


function reload_location_summary_sales(point_id){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

    var input_location_summary_sales_sales_index = document.getElementById('location_summary_sales_sales_index');
    var input_location_name = document.getElementById('input_location_name');
    var element_yearly_sales = document.getElementById('location_summary_sales_yearly_sales');
    var element_date_opening = document.getElementById('location_summary_sales_date_opening');
    var element_days_opened = document.getElementById('location_summary_sales_days_opened');
    var element_square_feet = document.getElementById('location_summary_sales_square_feet');
    var element_done_span = document.getElementById('location_summary_sales_done_span');
//notes
    var element_notes_owner = document.getElementById('notes_owner');
    var element_notes_contact = document.getElementById('notes_contact');
    var element_notes_address = document.getElementById('notes_address');
    var element_notes_price = document.getElementById('notes_price');
    var element_notes_area = document.getElementById('notes_area');
    var element_notes_tip_price = document.getElementById('notes_tip_price');
    var element_notes_tip_area = document.getElementById('notes_tip_area');
    var element_done_span2 = document.getElementById('location_summary_notes_done_span');
//notes

    $.ajax({
        url:'/project/get_point_sales',
        type: "POST",
        data: {'point_id': point_id},
        success:function(response){
            button_location_name.disabled = false;
            button_location_name.innerHTML = "Save name";
            if ('sales' in response){
                if ('sales' in response['sales']) {
                    element_yearly_sales.value = response['sales']['sales'];
                } else { 
                    element_yearly_sales.value = ''; 
                }
                if ('opening_date' in response['sales']) {
                    element_date_opening.value = response['sales']['opening_date'];
                } else { 
                    element_date_opening.value = ''; 
                }
                if ('opened_days' in response['sales']) {
                    element_days_opened.value = response['sales']['opened_days'];
                } else { 
                    element_days_opened.value = ''; 
                }
                if ('square_feet' in response['sales']) {
                    element_square_feet.value = response['sales']['square_feet'];
                } else { 
                    element_square_feet.value = ''; 
                }
            }
            //notes
            
            if ('notes' in response){
                if ('owner' in response['notes']) {
                    element_notes_owner.value = response['notes']['owner'];
                }else { 
                    element_notes_owner.value = ''; 
                }
                if ('contact' in response['notes']) {
                    element_notes_contact.value = response['notes']['contact'];
                }else { 
                    element_notes_contact.value = ''; 
                }
                if ('address' in response['notes']) {
                    element_notes_address.value = response['notes']['address'];
                }else { 
                    element_notes_address.value = ''; 
                }
                if ('price' in response['notes']) {
                    element_notes_price.value = response['notes']['price'];
                }else { 
                    element_notes_price.value = ''; 
                }
                if ('area' in response['notes']) {
                    element_notes_area.value = response['notes']['area'];
                } else { 
                    element_notes_area.value = ''; 
                }
                if ('tip_price' in response['notes']) {
                    element_notes_tip_price.value = response['notes']['tip_price'];
                } else { 
                    element_notes_tip_price.value = ''; 
                }
                if ('tip_area' in response['notes']) {
                    element_notes_tip_area.value = response['notes']['tip_area'];
                    
                } else { 
                    element_notes_tip_area.value = ''; 
                }
            //notes  */
            }
            element_done_span.innerText = '';
            element_done_span2.innerText = '';
        },
        error:function (xhr, textStatus, thrownError){}
        });
    }


function set_location_name(){
    var input_location_name = document.getElementById('input_location_name');
    var button_location_name = document.getElementById('button_location_name');
    var location_name = input_location_name.value;
    var point_id = selected_marker_id;
    console.log(point_id);

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});
    $.ajax({
        url:'/project/set_location_name/',
        type: "POST",
        data: {'point_id': point_id, 'location_name': location_name},
        success:function(response){
            if (response['response'] == 'OK'){
                load_score_board();
                button_location_name.disabled = true;
                button_location_name.innerHTML = 'Saved';
            } else {
                var error_message = response['error_message'];
                alert("Error\n" + error_message);
            }
        },
        error:function (xhr, textStatus, thrownError){}
        });
}

function location_summary_delete_point(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

    if (selected_marker_id > 0) {
        $.ajax({
            url:'/project/delete_point',
            type: "POST",
            data: {'point_id':selected_marker_id},
            success:function(response){
                for (var i = 0; i < markers.length; i++) {
                    if (markers[i].local_custom_point_id == selected_marker_id) {
                        markers[i].setMap(null);
                        selected_marker_id = -1;
                        selected_marker = null;
                        markers.splice(i, 1);
                        break;
                        }
                    }
                    if (pointer_marker != null){  //remove pointer
                        pointer_marker.setMap(null);
                    }
                    load_score_board();
                },
            error:function (xhr, textStatus, thrownError){}
            });
        }
    else {
        alert("unselected point");
        }
    }

function reload_location_summary_status(point_id){
    var select_status = document.getElementById('select_status');
    var input_location_name = document.getElementById('input_location_name');
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});
    $.ajax({
        url:'/project/get_point_data',
        type: "POST",
        data: {'point_id': point_id},
        success:function(response){
            if (response['response'] == 'OK'){
                if ('location_name' in response){
                    input_location_name.value = response['location_name'];
                } else {
                    input_location_name.value = '';
                }
                if ('status' in response){
                    var status = response['status'];
                    select_status.value = status;
                    change_color_div_status(status);
                }
            } else {
                //var error_message = response['error_message'];
                //alert("Error\n" + error_message);
            }
        },
        error:function (xhr, textStatus, thrownError){}
        });
    }


function make_hitscore_model(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

    var project_id = select_project.value;

    $.ajax({
        url:'/project/make_hitscore_model',
        type: "POST",
        data: {'project_id': project_id},
        success:function(response){
        },
        error:function (xhr, textStatus, thrownError){}
        });
    }



function update_location_summary_model_message(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

    var project_id = select_project.value;
    var element = document.getElementById('location_summary_hitscore_model');

    $.ajax({
        url:'/project/project_model_message',
        type: "POST",
        data: {'project_id': project_id},
        success:function(response){
            element.innerText = response['msg'];
        },
        error:function (xhr, textStatus, thrownError){}
        });
    }

function get_point_report(){
    var view_url = '/project/get_point_report/'
    var document_url = '';
    var csrftoken = getCookie('csrftoken');
    var point_id = selected_marker_id;
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});
    $.ajax({
        url: view_url,
        type: "POST",
        data: {'point_id': point_id},
        success:function(response){
            if ('report_url' in response){
                window.open(response['report_url'], '_blank');
            }
            if (response['response']  == 'error'){
                console.log("error al retornar al js");
                alert("Error.\n" + response['error_message'])
            }
        },
        error:function (xhr, textStatus, thrownError){}
        });
}

function get_project_report(){
    var view_url = '/project/get_project_report/'
    var document_url = '';
    var csrftoken = getCookie('csrftoken');
    var select_project = document.getElementById('select_project');
    var project_id = select_project.value;
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});
    $.ajax({
        url: view_url,
        type: "POST",
        data: {'project_id': project_id},
        success:function(response){
            if ('report_url' in response){
                window.open(response['report_url'], '_blank');
            } 
            if (response['response']  == 'error'){
                alert("Error.\n" + response['error_message'])
            }
        },
        error:function (xhr, textStatus, thrownError){}
        });
}



