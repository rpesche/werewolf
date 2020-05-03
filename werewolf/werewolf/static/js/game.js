
function set_action_to(klass, bootstrap_attribute, player) {
    var divs = document.getElementsByClassName(klass)
    for (var i = 0, len = divs.length; i < len; i++) {
        var div = divs[i];
        var button = div.children[0];

        var set_class = "btn-"  + bootstrap_attribute;
        var unset_class = "btn-outline-" + bootstrap_attribute;

        button.classList.remove(unset_class)
        button.classList.remove(set_class)

        if (div.id == player) {
            button.classList.add(set_class)
        } else {

            button.classList.add(unset_class)
        }
    }
}


function action(player, path, klass, bootstrap_btn) {
   csrf_token = Cookies.get('csrftoken');


   $.ajaxSetup({
    beforeSend: function(xhr, settings) {
         if (!/^https?:.*/.test(settings.url)  && settings.type == "POST") {
             xhr.setRequestHeader("X-CSRFToken",  csrf_token);
         }
     }
   })

   var url = window.location.pathname + path;
   $.ajax({
       method : 'POST',
       url : url,
       data : {
            'whom': player
       },
       dataType: 'json',
       success: function() {
            set_action_to(klass, bootstrap_btn, player);
       }
    });
}



function vote(player) {
    action(player, '/vote', "vote-btn", "success")
}
