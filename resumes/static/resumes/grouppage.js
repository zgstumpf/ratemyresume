document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll('table.datatables').forEach(function(table) {
        new DataTable(table);
    });

    $("#members-header").click(function(){
        $("#members-data").slideToggle("fast");
    });

    $("#join-request-header").click(function(){
        $("#join-request-data").slideToggle("fast");
    });

    $("#join-request-history-header").click(function(){
        $("#join-request-history-data").slideToggle("fast");
    });


    $("#invitation-header").click(function(){
        $("#invitation-data").slideToggle("fast");
    });

    $("#invitation-history-header").click(function(){
        $("#invitation-history-data").slideToggle("fast");
    });

});