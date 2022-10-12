(function ($) {
    "use strict";

    
    /*==================================================================
    [ Validate ]*/
    var fname = $('.validate-input input[name="Name"]');
    var email = $('.validate-input input[name="Email"]');
    var subject = $('.validate-input select[name="Topic"]');
    var message = $('.validate-input textarea[name="Message"]');


    $('.validate-form').on('submit',function(e){
        var check = true;

        if($(fname).val().trim() == ''){
            showValidate(fname);
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
            data: $(".app-form").serialize(),
            success: function(response) {
                
                if(response.result == "success") {
                    $('.app-form')[0].reset();
                    $('.overlay').css("visibility", "visible");
                    $('.overlay').css("opacity", "1");
                    return true;
                }
                else {
                    alert("Something went wrong. Please try again.")
                }
            },
            error: function() {
                
                alert("Something went wrong. Please try again.")
            }
        });
        
        if ($(fname).val() == 'Nathan Piveteau') {
            $('.masterpiece').css("max-width", "100%")
            $('.logo').css("max-width", "0")
        }
        else {
            $('.masterpiece').css("max-width", "0")
            $('.logo').css("max-width", "100%")
        }
    });


    $('.validate-form .app-form-control').each(function(){
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

    $(".close").on('click', function() {
        $('.masterpiece').css("max-width", "0")
        $('.logo').css("max-width", "0")
        $('.overlay').css("visibility", "hidden");
        $('.overlay').css("opacity", "0");
      });
    
    

})(jQuery);
