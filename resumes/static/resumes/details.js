document.addEventListener("DOMContentLoaded", () => {
    // Put all JS code in here
    // Make sure page-specific JS functions have different names than site-wide functions.
    var avgRating = $('#avgRatingForJS').text();
    var ownerUsernameForJS = $('#ownerUsernameForJS').text();
    var userRating = $('#userRatingForJS').text();
    var userRatingUpdatedAt = $('#userRatingDateForJS').text() // TODO: This needs to be updated at

    // This code executes as soon as the page loads. If userRating exists from database,
    // make the corresponding rating-option look selected.
    if (userRating) {
        visuallySelectRatingOption(userRating)
        // Also, change the text under the rating scale.
        youRatedThisResumeOn(userRatingUpdatedAt)
        showRatingScore(avgRating);
    } else {
        // User has not rated this resume yet
        $('#rating-description').text('Rate the resume relative to resumes of individuals with a similar education level and years of career experience.')
    }


    $('#commentForm').submit(function (event) {
        // This code runs the moment you press the submit button for the comment form

        // Some browsers may do a default action when an HTML form is submitted, such as refresh the page
        // This line prevents any unexpected behavior and gives us more control over what happens
        event.preventDefault();

        // Get value of action attribute of HTML form, which is the URL we will POST the data to
        // Why could hardcode the URL here, but it is better to let Django set the URL in the template,
        // and then borrow that URL since we can't use Django blocks in static files such as JavaScript
        var actionUrl = $(this).attr('action');

        // We want to submit the form and send the data to the backend without refreshing the whole page,
        // which is what AJAX helps with.
        $.ajax({
            data: $(this).serialize(), // Give AJAX the form data
            type: 'POST', // Submitting form will always be 'POST'
            url: actionUrl, // URL for AJAX to send data to
            headers: {'X-CSRFToken': getCsrf()},
            crossDomain: false,

            // Since we control the view connected to the URL, we determine if we the AJAX call
            // is a success or error.
            // If the view returns JsonResponse with status in the success range, typically 2xx,
            // the code in the success block executes.
            // Or, if status is in the error range, typically 4xx-5xx, the code in the error block
            // executes.
            success: function (response) {
                // response is the object set in the first parameter of JsonResponse
                // Example: {comment: 'nice'}

                // Clear write comment field
                $('#write-comment-input').val('')

                // Insert data from response into comments so user sees their data on the page without need for refresh
                comment = response.comment
                var commentHTML = `
                <div class="card">
                    <div class="card-body">
                        <p class="comment-user-header comment-username">${comment.user}</p>
                `
                if (comment.user===ownerUsernameForJS){
                    commentHTML += `
                        <p class="comment-user-header owner-designation">RESUME OWNER</p>
                    `
                }
                commentHTML += `
                        <p class="card-text">${comment.text}</p>
                        <p class="comment-user-header">${comment.created_at}</p>
                    </div>
                </div>
                `
                $("#scrollable-comments").prepend(commentHTML)
            },
            error: function (response) {
                console.error("Error happened in ajax")
            }
        });
    });

    $('#submit-comment-button').click(function() {
        $('#commentForm').submit()
    });

    $('#ratingForm').submit(function (event) {
        event.preventDefault();
        var actionUrl = $(this).attr('action');
        $.ajax({
            data: $(this).serialize(),
            type: 'POST',
            url: actionUrl,
            headers: {'X-CSRFToken': getCsrf()},
            crossDomain: false,
            success: function (response) {
                console.log(response)
                visuallySelectRatingOption(response.value)
                youRatedThisResumeOn(response.updated_at) // Date formatting is inconsistent
                showRatingScore(avgRating);
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

    /**
     * Changes description text under rating scale to say when user last rated resume.
     */
    function youRatedThisResumeOn(stringDate) {
        $('#rating-description').text(`You rated this resume on ${stringDate}`) // No period because date ends in period (ex: ... p.m.)
    }

    function showRatingScore(avgRating) {
        $('#rating-score').text(`The average rating is ${avgRating}`)
    }


});
// Any JS code after this point may execute before HTML finishes loading
// You shouldn't put JS code here unless you know what you're doing