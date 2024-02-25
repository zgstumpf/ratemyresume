document.addEventListener("DOMContentLoaded", () => {

    $('#signupForm').submit(function (event) {
        event.preventDefault();
        var actionUrl = $(this).attr('action');
        $.ajax({
            data: $(this).serialize(),
            type: 'POST',
            url: actionUrl,
            success: function (response) {
                window.location.href = response.redirectURL
            },
            error: function (response) {
                console.error(response.responseJSON.error)
            }
        });
    });






});