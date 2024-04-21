document.addEventListener("DOMContentLoaded", () => {
    $('.accept-invite').on('submit', function(event) {
        event.preventDefault()

        const form = $(this)
        const url = form.data('url')

        $.ajax({
            data: $(this).serialize(),
            type: 'POST',
            url: url,
            headers: {'X-CSRFToken': getCsrf()},
            crossDomain: false,
            success: function (response) {
                form.closest('.group-notif-card').remove()
                popupMsg(`You are now a member of ${response.group}.`)
            },
            error: function (response) {
                console.error(response.responseJSON.error)
            }
        })
    })

    $('.reject-invite').on('submit', function(event) {
        event.preventDefault()

        const form = $(this)
        const url = form.data('url')

        $.ajax({
            data: $(this).serialize(),
            type: 'POST',
            url: url,
            headers: {'X-CSRFToken': getCsrf()},
            crossDomain: false,
            success: function (response) {
                form.closest('.group-notif-card').remove()
            },
            error: function (response) {
                console.error(response.responseJSON.error)
            }
        })
    })


})