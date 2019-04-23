$(document).ready(function()
{
    if(document.getElementById('birthday'))
    {
        if(document.getElementById('birthday').value == "")
            document.getElementById('birthday').valueAsDate = new Date();
    }

    document.getElementById("loginContent").style = "display:none" 
        

    $('#user').keyup(function(){
        // var data = $("#title").serialize() //I have to send the form because it has the TOKEN to access URL
        // if($("#user")[0].value.length > 4)
        // {   
        var data = $("#regFormUser").serialize() //Send all form to the server
        $.ajax({
            method: "POST",
            url: "/checkUser",
            data: data,
        })
        .done(function(res){
            $('#errorMsg').html(res) //The URL check title returns dictionary inside the another dictionary
            //Inside res there is a dictionary ---> errors and more...
            //Inside errors there is a dictionary with Tags Errors and maybe more...
            if(res.errors.user)
            {
                $("#userError").text(res.errors.user)
                $("#btnSubForm").attr("disabled", true);
            }
            else
            {
                $("#userError").text("")
                $("#btnSubForm").attr("disabled", false);
            }
        })
    })

    $('#email').keyup(function(){
        // var data = $("#title").serialize() //I have to send the form because it has the TOKEN to access URL
        if($("#email")[0].value.length > 4)
        {
            var data = $("#regFormUser").serialize() //Send all form to the server
            $.ajax({
                method: "POST",
                url: "/checkEmail",
                data: data,
            })
            .done(function(res){
                $('#errorMsg').html(res) //The URL check title returns dictionary inside the another dictionary
                //Inside res there is a dictionary ---> errors and more...
                //Inside errors there is a dictionary with Tags Errors and maybe more...
                if(res.errors.email)
                {
                    $("#emailError").text(res.errors.email)
                    $("#btnSubForm").attr("disabled", true);
                }
                else
                {
                    $("#emailError").text("")
                    $("#btnSubForm").attr("disabled", false);
                }
            })
        }
    })
})

function sldTogg(control){
    getControl = document.getElementById(control);
    $(getControl).slideToggle("slow");
    event.preventDefault()
}


function validateForm()
{
    validation = true
    if(document.getElementById('fname').value.length < 2)
    {
        validation = false
        document.getElementById("fnameError").innerHTML = "The first name must be greater than 2 characters."
    }
    else
        document.getElementById("fnameError").style="display:none";


    if(document.getElementById('lname').value.length < 2)
    {
        validation = false
        document.getElementById("lnameError").innerHTML = "The last name must be greater than 2 characters."
    }
    else
        document.getElementById("lnameError").style="display:none";


    if(document.getElementById('email').value.length < 5)
    {
        validation = false
        document.getElementById("emailError").innerHTML = "A valid email is required."
    }
    else
        document.getElementById("emailError").style="display:none";

    
    if(document.getElementById('user').value.length < 5)
    {
        validation = false
        document.getElementById("userError").innerHTML = "A valid user is required."
    }
    else
        document.getElementById("userErr").style="display:none";

    today = new Date()
    birthday = document.getElementById('birthday').value
    birthday = new Date(birthday)

    var fecha1 = moment(birthday);
    var fecha2 = moment(today);
    if(fecha2.diff(fecha1, 'days') < 4750)
    {
        validation = false
        document.getElementById("birthdayError").innerHTML = "You should be greater than 13 years."
    }
    else
        document.getElementById("birthdayError").style="display:none";
    

    if(document.getElementById("password").value != document.getElementById("repassword").value 
        || document.getElementById("password").value == "" || document.getElementById("password").value.length < 8)
    {
        validation = false
        document.getElementById("passwordError").innerHTML = "The Passwords are wrong or short. Minimun 8 characters."
    }
    else
        document.getElementById("").style="display:none";

     if(!validation)
        event.preventDefault()
}