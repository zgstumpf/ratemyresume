document.addEventListener("DOMContentLoaded", () => {
    // Put all JS code in here
    // Make sure page-specific JS functions have different names than site-wide functions.




});
// Any JS code after this point will execute before HTML finishes loading
// You shouldn't put JS code here unless you know what you're doing
function toggleNavbar() {
    var navbar = document.getElementById("rmr-navbar");
    if (navbar.className === "rmr-navbar") {
      navbar.className += " responsive";
    } else {
      navbar.className = "rmr-navbar";
    }
}

// Source: https://docs.djangoproject.com/en/5.0/howto/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false
function getCsrf() {
    let name = 'csrftoken'
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Shows notification with green checkmark and custom text on the top of the screen.
 * Notification self-destructs after a timer.
 */
function popupMsg(text){
    $('.popup-msg').remove() // Clear any existing popup messages

    $("body").prepend(`
    <div class="popup-msg">
        <svg fill="#27d349" width="25px" height="25px" viewBox="-1.7 0 20.4 20.4" xmlns="http://www.w3.org/2000/svg" class="cf-icon-svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M16.417 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.917 7.917zm-4.105-4.498a.791.791 0 0 0-1.082.29l-3.828 6.63-1.733-2.08a.791.791 0 1 0-1.216 1.014l2.459 2.952a.792.792 0 0 0 .608.285.83.83 0 0 0 .068-.003.791.791 0 0 0 .618-.393L12.6 6.866a.791.791 0 0 0-.29-1.081z"></path></g></svg>
        <div>${text}<div>
    </div>
    <script>
        setTimeout(function() {
            $('.popup-msg').remove()
        }, 10000) // 10s
    </script>
    `)
}