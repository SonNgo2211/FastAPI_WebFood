
$(window).on('load', function(){
    getCart();
})

$('#button-addon1').on('click', function() {
    var oldValue = $('#proQty').val();
    if (oldValue > 0) {
        var newValue = parseInt(oldValue) - 1;
    } else {
        newValue = 0;
    } 
    $('#proQty').val(newValue)
});

$('#button-addon2').on('click', function(){
    var newValue = $('#proQty').val();
    $('#proQty').val(parseInt(newValue) + 1);
});

//add to cart

$('#add_to_cart').on('click', function() {
    var fid = $('#food_id').text();
    var qty = $('#proQty').val()
    $.ajax({
        url: "/carts/addToCart",
        type: "post",
        data: `{
            "fid": "${fid}",
            "qty": "${qty}"
        }`,
        contentType: "application/json",
        dataType: 'json',
        success: function(data) {
            getCart()
        },
        error: function(data) {
            alert("Sorry, error occurred!")
        }
    })
})

function getCart() {
    $.ajax({
        url: "/carts/getCart",
        type: "get",
        success: function(data) {
            $('#total_pro').text('$' + data.amount)
            if(data.cart != null) {
                $('#total_cart').text(data.cart['items'].length)
            } else {
                $('#total_cart').text(0)
            }
        },
        error: function(data) {
            alert("Sorry, error occurred!")
        }
    });
}
