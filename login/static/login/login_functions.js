var temp;
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


function sign_in(){
    var email = document.getElementById("signin_email").value;
    var passw = document.getElementById("signin_password").value;
    $.ajax({
        url:'/login/signin/',
        type: "POST",
        data: {'email': email, 'password':passw},
        success:function(response){
            if (response.status=="OK") {
                window.location = "/map";
                }
            else {
                alert(response.msg)
                }
            },
        complete:function(){},
        error:function (xhr, textStatus, thrownError){}
        });
    }


//this function is called when user clicks "sign up" button.
function sign_up(){
    var first_name = document.getElementById('signup_first_name').value;
    var last_name  = document.getElementById('signup_last_name').value;
    var email      = document.getElementById('signup_email').value;
    var password   = document.getElementById('singup_password').value;
    var terms      = document.getElementById('singup_terms').checked;

    if (first_name=="") {
        alert("you must enter your first name");
        }
    else if (last_name=="") {
        alert("you must enter your last name");
        }
    else if (email=="") {
        alert("you must enter your email");
        }
    else if (password=="") {
        alert("you must enter a password");
        }
    else if (terms==false) {
        alert("you must accept the terms and conditions");
        }
    else {
        $.ajax({
            url:'/login/useradd/',
            type: "POST",
            data: {'first_name':first_name, 'last_name':last_name, 'email':email, 'password':password, 'terms':terms},
            success:function(response){
                if(response.status=='OK') {
                    window.location = "/map";
                    }
                },
            complete:function(){},
            error:function (xhr, textStatus, thrownError){}
            });
        }
    }


