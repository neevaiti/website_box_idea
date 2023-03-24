$(document).ready(function () {
  $('.like-btn').click(function () {
    let ideaId = $(this).attr('data-id');
    let action = $(this).attr('data-action');

    $.ajax({
      url: '/idees/',
      type: 'POST',
      data: {
        'idea_id': ideaId,
        'action': action,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function (response) {
        $('.like-btn[data-id=' + ideaId + ']').attr('data-action', response.action);
        $('.like-btn[data-id=' + ideaId + ']').html(response.like_count + ' Likes');

        if (response.action === 'like') {
          $('.like-btn[data-id=' + ideaId + ']').removeClass('btn-outline-primary').addClass('btn-primary');
        } else {
          $('.like-btn[data-id=' + ideaId + ']').removeClass('btn-primary').addClass('btn-outline-primary');
        }
      },
      error: function(xhr, errmsg, err){
          console.log(xhr.status + ": " + xhr.responseText);
      }
    });
  });

  $('.dislike-btn').click(function () {
    let ideaId = $(this).attr('data-id');
    let action = $(this).attr('data-action');

    $.ajax({
      url: '/idees/',
      type: 'POST',
      data: {
        'idea_id': ideaId,
        'action': action,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function (response) {
        $('.dislike-btn[data-id=' + ideaId + ']').attr('data-action', response.action);
        $('.dislike-btn[data-id=' + ideaId + ']').html(response.dislike_count + ' Dislikes');

        if (response.action === 'dislike') {
          $('.dislike-btn[data-id=' + ideaId + ']').removeClass('btn-outline-danger').addClass('btn-danger');
        } else {
          $('.dislike-btn[data-id=' + ideaId + ']').removeClass('btn-danger').addClass('btn-outline-danger');
        }
      },
      error: function(xhr, errmsg, err){
          console.log(xhr.status + ": " + xhr.responseText);
      }
    });
  });
});
