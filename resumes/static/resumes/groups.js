document.addEventListener("DOMContentLoaded", () => {

    $('.group-card').click(function(){
        window.location.href = $(this).data('url')
    })


});


document.addEventListener("DOMContentLoaded", () => {

    $("#search").on('submit', function(event) {
        event.preventDefault()

        let url = $(this).attr('action');

        $.ajax({
            data: $(this).serialize(),
            type: 'GET',
            url: url,
            headers: {'X-CSRFToken': getCsrf()},
            crossDomain: false,
            success: function (response) {
                response = response.results.join(' ')
                $('#results-header').text('Results')
                $('#results-groups').html(response)

                $('.group-card').click(function(){
                    window.location.href = $(this).data('url')
                })

            },
            error: function (response) {
                console.error(response.responseJSON.error)
            }
        });
    })


})