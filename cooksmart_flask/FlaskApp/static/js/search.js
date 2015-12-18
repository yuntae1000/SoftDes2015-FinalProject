$(function() {
    $('#search').click(function() {
 
        $.ajax({
            url: '/search',
            data: "{'searchquery': $('#searchquery').val()}",
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
