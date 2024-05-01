document.addEventListener("DOMContentLoaded", () => {
   // Load preview images of resumes
    var resume_id_divs = $('.resume-id')
    resume_id_divs.each(function() {
        var $this = $(this)
        $.ajax({
            type: 'GET',
            url: $this.data('url'),
            crossDomain: false,
            success: function (response) {
                $this.next('.resume-image-skeleton').append(`<img src="${response.image}" style="max-width: 100%; max-height: ;">`);
                $this.next('.resume-image-skeleton').css("animation", "none");
            },
            error: function (response) {
                console.error(response.responseJSON.error)
            }
        });
    })


    // <div class="resume-card" data-detailsUrl="{% url 'details' resume.id %}">
    $('.resume-card').click(function(){
        // When I gave the blank upload card class="resume-card" so it would have right CSS, it also had the JS from here
        // applied to it. The blank card doesn't have a data-detailsURL; it has a data-url redirecting to upload page.
        if ($(this).data('url')) {
            window.location.href = $(this).data('url')
        }
        else {
            window.location.href = $(this).data('detailsurl')
        }
    })



    // Set color of rating icon
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

    var ratings = $('.resume-card-avgrating');
    ratings.each(function() {
        var $this = $(this);
        var val = parseFloat($this.text());

        var red = new Color(255, 0, 0),
            yellow = new Color(255, 255, 0),
            green = new Color(6, 170, 60),
            start, end;

        if (val <= 5) {
            start = red;
            end = yellow;
        } else {
            start = yellow;
            end = green;
            val -= 5; // Adjust rating value for the green range
        }

        var startColors = start.getColors(),
            endColors = end.getColors();
        var r = Interpolate(startColors.r, endColors.r, 5, val);
        var g = Interpolate(startColors.g, endColors.g, 5, val);
        var b = Interpolate(startColors.b, endColors.b, 5, val);

        var opacity = 0.75
        $this.css({
            backgroundColor: "rgba(" + r + "," + g + "," + b + "," + opacity + ")"
        });

    });




    tippy('.resume-card-menu', {
      content: '<a class="menu-option" href="#">Edit</a><button class="menu-option">Delete</button>',
      allowHTML: true,
      interactive: true,
      appendTo: () => document.body, // Fixes positioning
      placement: 'bottom',
      trigger: 'click',
    });


    // Separates clicking card and clicking menu actions.
    $('.resume-card-menu').click(function(event) {
        event.stopPropagation()
    })


});

