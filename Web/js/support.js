(function ($) {
    "use strict";

    
    /*==================================================================
    [ Validate ]*/
    var fname = $('.validate-input input[name="FIRSTNAME"]');
    var lname = $('.validate-input input[name="LASTNAME"]');
    var email = $('.validate-input input[name="E-MAIL"]');
    var subject = $('.validate-input input[name="TOPIC"]');
    var message = $('.validate-input textarea[name="MESSAGE"]');


    $('.validate-form').on('submit',function(e){
        var check = true;

        if($(fname).val().trim() == ''){
            showValidate(fname);
            check=false;
        }

        if($(lname).val().trim() == ''){
            showValidate(lname);
            check=false;
        }

        if($(subject).val().trim() == ''){
            showValidate(subject);
            check=false;
        }


        if($(email).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
            showValidate(email);
            check=false;
        }

        if($(message).val().trim() == ''){
            showValidate(message);
            check=false;
        }
        if(!check)
            return false;

        e.preventDefault();
      
        $.ajax({
            url: "https://script.google.com/macros/s/AKfycbym5HXOjVJZvqlpVhhcBDzB32kYO9-Qq9he6YyMTSqau3C0RqWTqut99HIDfHCjqCc/exec",
            method: "POST",
            dataType: "json",
            data: $(".contact1-form").serialize(),
            success: function(response) {
                
                if(response.result == "success") {
                    $('.contact1-form')[0].reset();
                    alert('Thank you for contacting us.');
                    return true;
                }
                else {
                    alert("Something went wrong. Please try again.")
                }
            },
            error: function() {
                
                alert("Something went wrong. Please try again.")
            }
        },
        console.log($(".contact1-form").serialize())
        )
    });


    $('.validate-form .input1').each(function(){
        $(this).focus(function(){
           hideValidate(this);
       });
    });

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    
    

})(jQuery);
