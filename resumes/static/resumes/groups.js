document.addEventListener("DOMContentLoaded", () => {

    $('.group-card').click(function(){
        window.location.href = $(this).data('url')
    })


});