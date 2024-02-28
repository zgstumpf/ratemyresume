document.addEventListener("DOMContentLoaded", () => {

    // This element will be hidden until user selects 'Shared With Specific Groups'
    // Unfortunately, this is hardcoded. This text must be the same as the label from forms.py -> UploadResumeForm -> line groupsSharedWith(label)
    // For some reason Django doesn't give the label an id
    $("p:contains('Share with the following groups:')").css('display', 'none')
    $("#id_visibility").change(function() {
        var visibilitySelection = $(this).val();
        if (visibilitySelection === 'shared_with_specific_groups') {
            $("p:contains('Share with the following groups:')").css('display', 'block')
            // Initially set to hidden in upload.css
            $('#id_groupsSharedWith').css('display', 'block')
        } else {
            $("p:contains('Share with the following groups:')").css('display', 'none')
            $('#id_groupsSharedWith').css('display', 'none')
        }
    });

    const placeholderVariations = [
        "Entry Web Developer",
        "Accounting Grad",
        "Computer Science Major",
        "CEO",
        "MBA Graduate",
        "Technical Resume",
        "Creative Resume",
        "Experienced Sales",
        "Sophomore, Biology Major",
        "Project-based",
        "Internship Resume",
        "Full-time Resume",
        "Philosophy PHD Seeking Retail Work"
    ];
    function randomizeNameInputPlaceholder(){
        const randomIndex = Math.floor(Math.random() * placeholderVariations.length);
        $("#id_name").attr("placeholder", placeholderVariations[randomIndex]);
    }
    setInterval(randomizeNameInputPlaceholder, 5000);




});