window.onload = function(){
    $(".prerow_div_ajax").on('click', 'a[type="button"]', function(){
        let trg = event.target;
        $.ajax({
            url: "/baskets/basket_add/" + trg.getAttribute("good_id"),
            success: function(data){
                if (typeof(data.login_url) !== "undefined"){
                    window.location.replace(data.login_url);
                }
            }
        });
    event.preventDefault();
    });

}