document.addEventListener("DOMContentLoaded", () => {
    var avgRating = $('#avgRatingForJS').text();
    var ownerUsernameForJS = $('#ownerUsernameForJS').text();
    var userRating = $('#userRatingForJS').text();
    var userRatingUpdatedAt = $('#userRatingDateForJS').text() // TODO: This needs to be updated at

    if (userRating) {
        visuallySelectRatingOption(userRating)
    } else {
        $('#rating-description').text('Rate the resume relative to resumes of individuals with a similar education level and years of career experience.')
    }


    $('#commentForm').submit(function (event) {
        event.preventDefault();

        const url = $(this).attr('action');

        $.ajax({
            data: $(this).serialize(),
            type: 'POST',
            url: url,
            headers: {'X-CSRFToken': getCsrf()},
            crossDomain: false,

            success: function (response) {
                $('#no-comments-placeholder').remove()
                $('.write-comment-input').val('')
                $('#comment-section').prepend(response.commentHtml)
            },
            error: function (response) {
                console.error(response.responseJSON.error)
            }
        });
    });


    $('#submit-comment-button').click(function() {
        $('#commentForm').submit()
    });


    $('#ratingForm').submit(function (event) {
        event.preventDefault();

        const url = $(this).attr('action');

        $.ajax({
            data: $(this).serialize(),
            type: 'POST',
            url: url,
            headers: {'X-CSRFToken': getCsrf()},
            crossDomain: false,
            success: function (response) {
                visuallySelectRatingOption(response.value)
                $('#rating-description').text('You rated this resume just now')
                popupMsg('Rating sent')
            },
            error: function (response) {
                console.error(response.responseJSON.error)
            }
        });
    });

    $(".rating-option").click(function(event) {
        // Get content, which is 0-10, of the specific rating option clicked.
        var value = $(this).text();
        $("#rating_form_value").val(value);
        $('#ratingForm').submit()
    })

    /**
     * value must be 0-10, corresponding to rating option.
     */
    function visuallySelectRatingOption(value){
        // If existing option(s) is selected, unselect it.
        $('.rating-option-selected').removeClass("rating-option-selected")

        $(`.rating-option[data-value="${value}"]`).addClass("rating-option-selected")
    }

});
