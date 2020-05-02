
function post_vote(data) {
    // TODO : highlight current elected character
}


function vote(player) {
   csrf_token = Cookies.get('csrftoken');


   $.ajaxSetup({
    beforeSend: function(xhr, settings) {
         if (!/^https?:.*/.test(settings.url)  && settings.type == "POST") {
             xhr.setRequestHeader("X-CSRFToken",  csrf_token);
         }
     }
   })

   var url = window.location.pathname + '/vote'
   $.ajax({
       method : 'POST',
       url : url,
       data : {
            'whom': player
       },
       dataType: 'json',
       success: post_vote
    });
}
