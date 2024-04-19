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


                // Get images and style ratings for each resume in search results
                // We are doing same thing here as when resume_card.js is loaded for first time
                // Atrocious repeating code, improve later.
                var resume_id_divs = $('#ajax-resumes .resume-card .resume-id')
                resume_id_divs.each(function() {
                    var $this = $(this)
                    $.ajax({
                        type: 'GET',
                        url: $this.data('url'),
                        crossDomain: false,
                        success: function (response) {
                            $this.next('.resume-image-skeleton').append(`<img src="${response.image}" style="max-width: 100%; max-height: ;">`);
                            $this.next('.resume-image-skeleton').css("animation", "none");
                        },
                        error: function (response) {
                            console.error(response.responseJSON.error)
                        }
                    });
                })

                $('#ajax-resumes .resume-card').click(function(){
                    window.location.href = $(this).data('detailsurl')
                })



                
            },
            error: function (response) {
                console.error(response.responseJSON.error)
            }
        });
    })


})