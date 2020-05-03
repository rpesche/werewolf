
function set_vote_to(player) {
    var divs = document.getElementsByClassName("vote-btn")
    for (var i = 0, len = divs.length; i < len; i++) {
        var div = divs[i];
        var button = div.children[0];

        button.classList.remove("btn-outline-success")
        button.classList.remove("btn-success")

        if (div.id == player) {
            button.classList.add("btn-success")
        } else {

            button.classList.add("btn-outline-success")
        }
    }
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
       success: function() {
            set_vote_to(player);
       }
    });
}
