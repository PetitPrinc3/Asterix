$('.contact1-form').on('submit',function(e){
    //optional validation code here

    e.preventDefault();
  
    $.ajax({
        url: "https://script.google.com/macros/s/AKfycbx1qiP9FDriyv9Mps9mD1SPYVd6hIO75yCJktNDbgKVHbOyehzNkMJAIP-DwoFkqWZQ/exec",
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
    })
});