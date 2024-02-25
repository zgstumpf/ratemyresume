document.addEventListener("DOMContentLoaded", () => {

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