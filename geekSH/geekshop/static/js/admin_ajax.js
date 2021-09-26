window.onload = function(){
    $(".sb-sidenav").on("click", 'a[class="nav-link ajax_users"]', function(){
        $.ajax({
            url: "/admins/users/",
            success: function(data){
                $('div[id="layoutSidenav_content"]').html(data.result)

                $("tbody").on("click", "a[class='ajax_entity_update']", function(){
                    let trg = event.target;
                    $.ajax({
                        url: "/admins/user_update/" + trg.getAttribute("user_id"),
                        data: {"pk": trg.getAttribute("user_id")},
                        success: function(data){
                            $('div[id="layoutSidenav_content"]').html(data.result)
                            //save function
                            update_user()
                            //delete function
                            delete_user()
                        }
                    });
                    event.preventDefault();
                });

                $(".card-footer").on("click", 'button[class="btn btn-success ajax_entity_create"]', function(){
                    $.ajax({
                        url: "/admins/user_create/",
                        success: function(data){
                            $('div[id="layoutSidenav_content"]').html(data.result)
                            create_user()
                        }
                    });
                    event.preventDefault();
                });
            }
        });
        event.preventDefault();
    });
    $(".sb-sidenav").on("click", 'a[class="nav-link ajax_products"]', function(){
        $.ajax({
            url: "/admins/product_show/",
            success: function(data){
                $('div[id="layoutSidenav_content"]').html(data.result)
                }
        });
        event.preventDefault();
    });
    $(".sb-sidenav").on("click", 'a[class="nav-link ajax_categories"]', function(){
        $.ajax({
            url: "/admins/category_show/",
            success: function(data){
                $('div[id="layoutSidenav_content"]').html(data.result)
                }
        });
        event.preventDefault();
    });


    $(".sb-sidenav").on("click", 'td[class="ajax_entity_update"]', function(){
        $.ajax({
            url: "/admins/user_update/",
            success: function(data){
                $('div[id="layoutSidenav_content"]').html(data.result)
                }
        });
        event.preventDefault();
    });

}

let create_user = function(){
    $("form").on("submit", function(){
        $.ajax({
            url: "/admins/user_create/",
            headers: {"X-CSRFToken": $.cookie("csrftoken")},
            data: $(this).serialize(),
//            data: $("form").serializeArray(),
            success: function(data){
                $('div[id="layoutSidenav_content"]').html(data.result)
            },
            type: "POST"
        });
        event.preventDefault();
    });
}

let update_user = function(){
     $("#ajax-id").on("submit", function(){
        let trg = event.target;
        $.ajax({
            url: "/admins/user_update/" + trg.getAttribute("user_id"),
            headers: {"X-CSRFToken": $.cookie("csrftoken")},
            data: $("form").serializeArray(),
            success: function(data){
                $('div[id="layoutSidenav_content"]').html(data.result)
            },
            type: "POST"
        });
        event.preventDefault();
    });
}

let delete_user = function(){
    let trg = event.target;
     $("form").on("click", 'input[id="ajax-delete"]', function(){
        $.ajax({
            url: "/admins/user_delete/" + trg.getAttribute("user_id"),
            headers: {"X-CSRFToken": $.cookie("csrftoken")},
            success: function(data){
                $('div[id="layoutSidenav_content"]').html(data.result)
            },
            type: "DELETE"
        });
        event.preventDefault();
    });
}