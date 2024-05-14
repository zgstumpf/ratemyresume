// add JavaScript for any group cards that exist on the page
document.addEventListener("DOMContentLoaded", () => {
    $('.group-card').each((_, groupCard) => {
        addJavaScriptFunctionalityToGroupCard(groupCard)
    })
});

function addJavaScriptFunctionalityToGroupCard(groupCard){
    $(groupCard).click(function(){
        window.location.href = $(this).data('url')
    })
}