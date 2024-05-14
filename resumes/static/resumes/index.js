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
                $('#results-resumes').html(`<div id="ajax-resumes" class="resume-card-container">${response}</div>`)

                // We are doing same thing here as when resume_card.js is loaded for first time
                $('#ajax-resumes .resume-card').each((_, resumeCard) => {
                    addJavaScriptFunctionality(resumeCard)
                })
            },
            error: function (response) {
                console.error(response.responseJSON.error)
            }
        });
    })


})