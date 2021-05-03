$(function () {
    $('.cmt_btn').on('click', function () {
        var objId = $(this).attr('footer-id');
        $('#footer_' + objId).slideToggle("slow")
        
       
    });
});


$('.like-form').submit(function(e){
    e.preventDefault()

    const post_id = $(this).attr('id')   
    const url = $(this).attr('action')
    const thumbcolor = $(`.thumb${post_id}`).css('color')
    
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'post_id':post_id,
        },
        success: function(response) {           
     
            if(thumbcolor === 'rgb(0, 0, 0)') {
                $(`.thumb${post_id}`).css('color', 'blue');
            } else {
                $(`.thumb${post_id}`).css('color', 'black');
            }

            $(`.like-count${post_id}`).text(response.likes)
        },
        error: function(response) {
            console.log('error', response)
        }
    })

})


$('.share-form').submit(function(e){
    e.preventDefault()

    const post_id = $(this).attr('id')   
    const url = $(this).attr('action')
    const sharecolor = $(`.share${post_id}`).css('color')
    
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'post_id':post_id,
        },
        success: function(response) {           
     
            if(sharecolor === 'rgb(0, 0, 0)') {
                $(`.share${post_id}`).css('color', 'blue');
            } else {
                $(`.share${post_id}`).css('color', 'black');
            }

            $(`.share-count${post_id}`).text(response.shares)
        },
        error: function(response) {
            console.log('error', response)
        }
    })

})