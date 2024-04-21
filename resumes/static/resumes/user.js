document.addEventListener("DOMContentLoaded", () => {

    $('.resume-name-in-table').hover(async function mouseEntersElement(MouseEvent){
        // Remember, <img> is inside .resume-name-in-table element, which is why preview doesn't go away even if you hover off the name
        // and hover onto the preview image.
        hoverTimer = setTimeout(function(){
            // This code is activated after 750 ms
            $(MouseEvent.currentTarget).find(".resume-image-preview").css({
                // without -10, image is in bottom-right corner of cursor, and sometimes you may trigger mouseLeavesElement
                // as you try to move to the image. -10 moves image a little bit in the top-left direction
                top: MouseEvent.pageY - 10,
                left: MouseEvent.pageX - 10
            }).show();
        }, 750)
    }, async function mouseLeavesElement(mouseEvent){
        // Cancel showing of resume image preview - without this, preview would appear near your cursor even
        // if you moved it away after hovering
        clearTimeout(hoverTimer);
        $(this).find(".resume-image-preview").hide()
    })


    $('.blank-upload-card').click(function () {
        console.log('lll')
        console.log($(this).data('url'))
        // window.location.href = $(this).data('url')
    })

});