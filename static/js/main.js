jQuery(document).ready(function ($) {

    $('.go__vote .vote').on('click', function (e) {
        let user = $(this).data('user')
        let film = $(this).data('film')
        let rating = $(this).data('rating')

        let target = $(this)
        $.ajax({
            url: '/kino/vote/',
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
})