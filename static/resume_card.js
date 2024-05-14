document.addEventListener("DOMContentLoaded", () => {
    $('.resume-card').each((_, resumeCard) => {
        addJavaScriptFunctionality(resumeCard)
    })
});

function addJavaScriptFunctionality(resumeCard){
    loadPreviewImage(resumeCard)
    setClickListeners(resumeCard)
    addMenuTooltip(resumeCard)
    colorRating(resumeCard)
}

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

function addMenuTooltip(resumeCard){
    tippy($(resumeCard).find('.resume-card-menu')[0], {
        content: '<a class="menu-option" href="#">Edit</a><button class="menu-option">Delete</button>',
        allowHTML: true,
        interactive: true,
        appendTo: () => document.body, // Fixes positioning
        placement: 'bottom',
        trigger: 'click',
      });
}

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
        endColors = end.getColors();
    var r = Interpolate(startColors.r, endColors.r, 5, rating);
    var g = Interpolate(startColors.g, endColors.g, 5, rating);
    var b = Interpolate(startColors.b, endColors.b, 5, rating);

    var opacity = 0.75
    $this.css({
        backgroundColor: "rgba(" + r + "," + g + "," + b + "," + opacity + ")"
    });
}