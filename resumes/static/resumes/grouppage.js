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

    // Load preview images of resumes
    var resume_id_divs = $('.resume-id')
    resume_id_divs.each(function() {
        var $this = $(this)
        $.ajax({
            type: 'GET',
            url: $this.data('url'),
            crossDomain: false,
            success: function (response) {
                $this.next('.resume-image-skeleton').html(`<img src="${response.image}" style="max-width: 100%; max-height: ;">`);
                $this.next('.resume-image-skeleton').css("animation", "none");
            },
            error: function (response) {
                console.error(response.responseJSON.error)
            }
        });
    })


    // <div class="resume-card" data-detailsUrl="{% url 'details' resume.id %}">
    $('.resume-card').click(function(){
        window.location.href = $(this).data('detailsurl')
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
            console.log('... inviting user')
            event.preventDefault()

            var url = $(this).attr('action');
            console.log('csrf', getCsrf())
            $.ajax({
                data: $(this).serialize(),
                type: 'POST',
                url: url,
                headers: {'X-CSRFToken': getCsrf()},
                crossDomain: false,
                success: function (response) {
                    console.log(response)
                    popupMsg("Your invite was successfully sent.")
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