document.addEventListener("DOMContentLoaded", () => {
    // Put all JS code in here
    // Make sure page-specific JS functions have different names than site-wide functions.


    $('#commentForm').submit(function (event) {
        // This code runs the moment you press the submit button for the comment form

        // Some browsers may do a default action when an HTML form is submitted, such as refresh the page
        // This line prevents any unexpected behavior and gives us more control over what happens
        event.preventDefault();

        // Get value of action attribute of HTML form, which is the URL we will POST the data to
        // Why could hardcode the URL here, but it is better to let Django set the URL in the template,
        // and then borrow that URL since we can't use Django blocks in static files such as JavaScript
        var actionUrl = $(this).attr('action');

        // We want to submit the form and send the data to the backend without refreshing the whole page,
        // which is what AJAX helps with.
        $.ajax({
            data: $(this).serialize(), // Give AJAX the form data
            type: 'POST', // Submitting form will always be 'POST'
            url: actionUrl, // URL for AJAX to send data to

            // Since we control the view connected to the URL, we determine if we the AJAX call
            // is a success or error.
            // If the view returns JsonResponse with status in the success range, typically 2xx,
            // the code in the success block executes.
            // Or, if status is in the error range, typically 4xx-5xx, the code in the error block
            // executes.
            success: function (response) {
                // response is the object set in the first parameter of JsonResponse
                // Example: {comment: 'nice'}
                // Insert data from response into HTML so user sees their data on the page
                // without need for refresh
                console.log(response)
            },
            error: function (response) {
                console.error("Error happened in ajax")
            }
        });
    });

    $('#ratingForm').submit(function (event) {
        event.preventDefault();
        var actionUrl = $(this).attr('action');
        $.ajax({
            data: $(this).serialize(),
            type: 'POST',
            url: actionUrl,
            success: function (response) {
                console.log(response)
            },
            error: function (response) {
                console.error("Error happened in ajax")
            }
        });
    });

    // Code for comment section
    const commentSection = $('#comment-section');
    const itemsPerPage = 6; // set number of items per page
    let currentPage = 0;
    const items = commentSection.find('.card');

    function showPage(page) {
        const startIndex = page * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        items.each((index, item) => {
            $(item).toggleClass('hidden', index < startIndex || index >= endIndex);
        });
        updateActiveButtonStates();
    }

    function createPageButtons() {
        const totalPages = Math.ceil(items.length / itemsPerPage);
        const paginationContainer = $('<div class="pagination"></div>');
        const paginationButtonsGroup = $('<div class="page-buttons-group"></div>');
        paginationContainer.append(paginationButtonsGroup);
        paginationContainer.appendTo(commentSection);

        // Add page buttons
        for (let i = 0; i < totalPages; i++) {
            const pageButton = $('<button class="pagination">' + (i + 1) + '</button>');
            pageButton.on('click', function () {
                currentPage = i;
                showPage(currentPage);
                updateActiveButtonStates();
            });

            paginationButtonsGroup.append(pageButton);
        }
    }

    function updateActiveButtonStates() {
        const pageButtons = document.querySelectorAll('.pagination button');
        pageButtons.forEach((button, index) => {
            if (index === currentPage) {
            button.classList.add('active');
            } else {
            button.classList.remove('active');
            }
        });
    }

    createPageButtons(); // Call this function to create the page buttons initially
    showPage(currentPage);
    // End code for comment section

});
// Any JS code after this point will execute before HTML finishes loading
// You shouldn't put JS code here unless you know what you're doing