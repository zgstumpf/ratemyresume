document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll('table.datatables').forEach(function(table) {
        new DataTable(table);
    });

    $("#members-header").click(function(){
        $("#members-data").slideToggle("fast");
    });


    $("#send-request-form").submit(function(){
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
                $("#send-request-form").remove()
                popupMsg("Your join request was successfully sent.")
            },
            error: function (response) {
                console.error(response.responseJSON.error)
                $("#send-request-form-error").html(`${response.responseJSON.error}`)
            }
        });
    });

    $('.resume-card').each((_, resumeCard) => {
        addJavaScriptFunctionality(resumeCard)
    })


    // Create new query whenever user types in search bar
    $('#inviteUsersSearchBar').on('input', function() {
        query = $(this).val()
        $('#searchUsersToInviteForm').submit()
    });

    $('#searchUsersToInviteForm').on('submit', function(event) {
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
                $('#userResults').html(response)
                readyInviteForms()
            },
            error: function (response) {
                console.error(response.responseJSON.error)
            }
        });
    })

    function readyInviteForms() {
        $('.inviteUserForm').on('submit', function(event) {
            event.preventDefault()

            const url = $(this).attr('action');
            let form = $(this)

            console.log('csrf', getCsrf())
            $.ajax({
                data: $(this).serialize(),
                type: 'POST',
                url: url,
                headers: {'X-CSRFToken': getCsrf()},
                crossDomain: false,
                success: function (response) {
                    popupMsg("Your invite was successfully sent.")
                    form.closest('.invite-user-container').remove()
                },
                error: function (response) {
                    console.error(response.responseJSON.error)
                }
            });
        })
    }


    $('#inviteModal').on('hide.bs.modal', function () {
        $('#inviteUsersSearchBar').val('')
        $('#userResults').html('')
    });



});