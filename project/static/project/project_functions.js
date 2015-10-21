
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

function set_permissions(user_id, project_id, new_permissions){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
	$.ajax({
        url:'/project/projectuser_set_permissions/',
        type: "POST",
        data: { 'user_to_set_id':user_id,
                'project_id': project_id,
                'new_permissions': new_permissions
              },
        success:function(response){
                var img_permissions = document.getElementById('img_permissions_' + user_id)
                var a_permissions = document.getElementById('a_permissions_' + user_id);
                var p_permissions = document.getElementById('p_permissions_' + user_id);
                var p_error_message = document.getElementById('p_error_message');
                if (response['response'] == 'error'){
                     p_error_message.textContent = response['error_message'];
                     return;
                }
                if (new_permissions == 1){
                    img_permissions.src = '/static/project/images/read.png';
                    img_permissions.title = 'Set permissions to read only';
                    a_permissions.onclick = function () { 
                        set_permissions(user_id, project_id, 2 );
                        return false;
                    };
                    p_permissions.textContent = 'read and write';
                } else if (new_permissions == 2) {
                    img_permissions.src = '/static/project/images/write.png';
                    img_permissions.title = 'Set permissions to read and write';
                    a_permissions.onclick = function () { 
                        set_permissions(user_id, project_id, 1 );
                        return false;
                    };
                    p_permissions.textContent = 'read only';
                }
            },
        complete:function(){},
        error:function (xhr, textStatus, thrownError){}
    });
}


function add_user(project_id){
    var input_new_user_mail = document.getElementById('input_new_user_mail');
    var new_user_mail = input_new_user_mail.value.trim();
    var csrftoken = getCookie('csrftoken');
    
        $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    $.ajax({
        url:'/project/add_user/',
        type: "POST",
        data: { 'project_id': project_id,
                'new_user_mail': new_user_mail
              },
        success:function(response){
                var p_error_message = document.getElementById('p_error_message');
                var table_project_users = document.getElementById('table_project_users');
                var new_row, cell_mail, cell_permissions, cell_buttons;
                var project_id, user_id, project_user_id, user_mail;
                if (response['response'] == 'error'){
                    p_error_message.textContent = response['error_message'];
                } else if (response['response'] == 'OK'){
                    //get data of the new project_user
                    project_id = response['project_id'];
                    user_id = response['user_id'];
                    project_user_id = response['project_user_id'];
                    user_mail = response['user_mail'];
                    //insert row
                    p_error_message.textContent = "";
                    new_row = table_project_users.insertRow(1);
                    cell_mail = new_row.insertCell(0);
                    cell_permissions = new_row.insertCell(1);
                    cell_buttons = new_row.insertCell(2);
                    //add content to new row
                    new_row.id="tr_" + project_user_id;
                    cell_mail.textContent = user_mail;
                    cell_permissions.innerHTML = '<p id="p_permissions_' + user_id + '"> read only </p>';
                    cell_buttons.innerHTML =    '<a id="a_delete_' +  user_id + '" href="#" onClick="delete_user(' + project_user_id + ', \'tr_' + project_user_id + '\' );return false;">' +
                                                '<img id="img_delete_' + user_id + '" src="/static/project/images/delete.png" height="16" width="16" title="Delete user from project" />'+
                                                '</a>' + 
                                                "<a id='a_permissions_"+ user_id + "' href='#' onClick='set_permissions(" + user_id + ", " + project_id + ", 1 );return false;'>" +
                                                "<img id='img_permissions_" + user_id + "' src='/static/project/images/write.png'  height='16' width='16' title='Set permissions to read and write' />" +
                                                "</a>";
                                
                }
            },
        complete:function(){},
        error:function (xhr, textStatus, thrownError){}
    });
}

function delete_user(project_user_id, row_index){
    var tr_to_del = document.getElementById(row_index);
    var table_project_users = document.getElementById('table_project_users');
    var csrftoken = getCookie('csrftoken');
    
        $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    $.ajax({
    url:'/project/delete_user/',
    type: "POST",
    data: { 'project_user_id': project_user_id
          },
    success:function(response){
            var p_error_message = document.getElementById('p_error_message');
            if (response['response'] == 'error'){
                p_error_message.textContent = response['error_message'];
            } else if (response['response'] == 'OK'){
                p_error_message.textContent = "";
                table_project_users.deleteRow(tr_to_del.rowIndex);
            }
        },
    complete:function(){},
    error:function (xhr, textStatus, thrownError){}
    }); 
}
