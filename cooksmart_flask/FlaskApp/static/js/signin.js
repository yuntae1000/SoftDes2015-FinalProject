$(function() {
    $('#btnsignin').click(function() {
 
        $.ajax({
            url: '/Authenticate',
            data: "{'username': $('#username').val(),'password':$('#password').val()}",
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});