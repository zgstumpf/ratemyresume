document.addEventListener("DOMContentLoaded", () => {
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




});

