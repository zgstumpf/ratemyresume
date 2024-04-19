document.addEventListener("DOMContentLoaded", () => {

    $("#search").on('submit', function(event) {
        event.preventDefault()

        let url = $(this).attr('action');

        $.ajax({
            data: $(this).serialize(),
            type: 'GET',
            url: url,
            headers: {'X-CSRFToken': getCsrf()},
            crossDomain: false,
            success: function (response) {
                response = response.results.join(' ')
                $('#results-header').text('Results')
                $('#results-resumes').html(`<div id="ajax-resumes" class="resume-card-container">${response}</div>`)


                // Get images and style ratings for each resume in search results
                // We are doing same thing here as when resume_card.js is loaded for first time
                // Atrocious repeating code, improve later.
                var resume_id_divs = $('#ajax-resumes .resume-card .resume-id')
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

                $('#ajax-resumes .resume-card').click(function(){
                    window.location.href = $(this).data('detailsurl')
                })


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

                var ratings = $('#ajax-resumes .resume-card-avgrating');
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



            },
            error: function (response) {
                console.error(response.responseJSON.error)
            }
        });
    })


})