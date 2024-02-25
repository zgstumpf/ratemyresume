document.addEventListener("DOMContentLoaded", () => {
    // Put all JS code in here
    // Make sure page-specific JS functions have different names than site-wide functions.




});
// Any JS code after this point will execute before HTML finishes loading
// You shouldn't put JS code here unless you know what you're doing


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