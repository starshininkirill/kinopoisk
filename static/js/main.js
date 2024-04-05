jQuery(document).ready(function ($) {

    $('.go__vote .vote').on('click', function (e) {
        let user = $(this).data('user')
        let film = $(this).data('film')
        let rating = $(this).data('rating')

        let target = $(this)
        $.ajax({
            url: '/vote/',
            type: 'POST',
            dataType: 'json',
            data: {
                'user': user,
                'film': film,
                'rating': rating
            },
            success: function (response) {

                location.reload()
            }
        });
    })

    $('.review__bottom:not(.anonim) .review__rating').on('click', function () {
        let type = $(this).data('type')
        let film = $(this).closest('.review__bottom').data('film');
        let user = $(this).closest('.review__bottom').data('user');
        let review = $(this).closest('.review__bottom').data('review');
        th = $(this)
        $.ajax({
            url: '/set-review-rating/',
            type: 'POST',
            dataType: 'json',
            data: {
                'user': user,
                'film': film,
                'review': review,
                'type': type
            },
            success: function (response) {
                console.log(response.status);
                let newVal = NaN
                if (response.no_changed) {
                    return
                }
                if (!response.created) {
                    th.closest('.review__bottom').find('.review__rating span').each(function () {
                        let curentVal = $(this).text()
                        $(this).text(curentVal - 1)
                        $(this).closest('.review__rating').removeClass('active')
                        newVal = Number(th.find('span').text()) + 2
                    })
                } else {
                    newVal = Number(th.find('span').text()) + 1
                }

                th.find('span').text(newVal)
                th.addClass('active')

            }
        });
    })
}) 