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
                console.log(response)
                response = response.results.join(' ')
                $('#results-header').text('Results')
                $('#results-resumes').html(`<div class="resume-card-container">${response}</div>`)
            },
            error: function (response) {
                console.error(response.responseJSON.error)
            }
        });
    })


})