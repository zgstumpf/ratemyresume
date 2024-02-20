document.addEventListener("DOMContentLoaded", () => {
    // Put all JS code in here
    // Make sure page-specific JS functions have different names than site-wide functions.
    console.log("details.js loaded")


    $('#commentForm').submit(function (event) {
        event.preventDefault();
        // (?) I'm not sure how JavaScript knows the data is called resumeID
        // if the custom data field is data-resume-id
        var resume_id = $(this).data('resumeId');
        var actionUrl = $(this).attr('action');
        console.log(actionUrl);
        $.ajax({
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: actionUrl,
            success: function (response) {
                console.log(response)
            },
            error: function (response) {
                console.error("Error happened in ajax")
            }
        });
        return false;
    });


});
// Any JS code after this point will execute before HTML finishes loading
// You shouldn't put JS code here unless you know what you're doing