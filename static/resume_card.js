// add JavaScript for any resume cards that exist on the page
document.addEventListener("DOMContentLoaded", () => {
    $('.resume-card').each((_, resumeCard) => {
        addJavaScriptFunctionality(resumeCard)
    })
});


/**
 * Applies JavaScript for a resume card (any element with class `resume-card`)
 * - Loads preview image.
 * - Enables redirects by clicking.
 * - Generates tooltip for menu icon.
 * - Applies background color to the rating metric.
 */
function addJavaScriptFunctionality(resumeCard){
    loadPreviewImage(resumeCard)
    setClickListeners(resumeCard)
    addMenuTooltip(resumeCard)
    colorRating(resumeCard)
}

/**
 * Fetches resume screenshot via AJAX and replaces the loading animation.
 */
function loadPreviewImage(resumeCard){
    $.ajax({
        type: 'GET',
        url: $(resumeCard).find('.resume-id').data('url'),
        crossDomain: false,
        success: function (response) {
            imageSkeleton = $(resumeCard).find('.resume-image-skeleton')
            imageSkeleton.append(`<img src="${response.image}" style="max-width: 100%; max-height: ;">`);
            imageSkeleton.css("animation", "none");
        },
        error: function (response) {
            console.error(response.responseJSON.error)
        }
    });
}

/**
 * Enables redirecting to a resume's page when the card is clicked.
 */
function setClickListeners(resumeCard){
    $(resumeCard).click(function () {
        // When I gave the blank upload card class="resume-card" so it would have right CSS, it also had the JS from here
        // applied to it. The blank card doesn't have a data-detailsURL; it has a data-url redirecting to upload page.
        $(this).data('url') ? window.location.href = $(this).data('url') : window.location.href = $(this).data('detailsurl')
    })

    // When menu button is clicked, do not also register it as a click to the resume card.
    $(resumeCard).find('.resume-card-menu').click(function(event) {
        event.stopPropagation()
    })
}

/**
 * Uses {@link https://atomiks.github.io/tippyjs/|Tippy.js} to generate the Edit and Delete options when the menu icon is clicked.
 */
function addMenuTooltip(resumeCard){
    tippy($(resumeCard).find('.resume-card-menu')[0], {
        content: `<a class="menu-option" href="${$(resumeCard).data('edit-url')}">Edit</a><button class="menu-option">Delete</button>`,
        allowHTML: true,
        interactive: true,
        appendTo: () => document.body, // Fixes positioning
        placement: 'bottom',
        trigger: 'click',
      });
}

/**
 * Sets the background color of the rating.
 */
function colorRating(resumeCard){
    function Interpolate(start, end, steps, count) {
        var s = start,
            e = end,
            final = s + (((e - s) / steps) * count);
        return Math.floor(final);
    }

    function Color(_r, _g, _b) {
        var r, g, b;
        var setColors = function(_r, _g, _b) {
            r = _r;
            g = _g;
            b = _b;
        };

        setColors(_r, _g, _b);
        this.getColors = function() {
            var colors = {
                r: r,
                g: g,
                b: b
            };
            return colors;
        };
    }

    var red = new Color(255, 0, 0),
        yellow = new Color(255, 255, 0),
        green = new Color(6, 170, 60),
        start,
        end;

    var $this = $(resumeCard).find('.resume-card-avgrating');
    var rating = parseFloat($this.text());

    if (rating <= 5) {
        start = red;
        end = yellow;
    } else {
        start = yellow;
        end = green;
        rating -= 5; // Adjust rating value for the green range
    }

    var startColors = start.getColors(),
        endColors = end.getColors(),
        r = Interpolate(startColors.r, endColors.r, 5, rating),
        g = Interpolate(startColors.g, endColors.g, 5, rating),
        b = Interpolate(startColors.b, endColors.b, 5, rating);

    const opacity = 0.75
    $this.css({
        backgroundColor: "rgba(" + r + "," + g + "," + b + "," + opacity + ")"
    });
}
