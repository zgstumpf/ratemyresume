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
 * Returns HTML for a green popup message box that appears in the top left, with a close button that removes
 * the box when clicked.
 */
function popupMsg(text){
    $("body").prepend(`
    <div class="popup-msg">
        ${text}
        <span class="close-btn" onclick="removePopupMsg(this)">&times;</span>
    </div>
    <script>
        function removePopupMsg(btn) {
            $(btn).closest('.popup-msg').remove();
        }
    </script>
    `)
}