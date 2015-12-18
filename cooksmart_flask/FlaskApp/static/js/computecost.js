$(function() {
    $('#computecost').click(function() {
        $.ajax({
            url: '/computecost',
            data: "{'nofserving': $('#nofserving').val(),'selectedresult':$('selectedresult').val()}",
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
            // dataType: 'json'
            // contentType: "application/json"
        });
    });
});