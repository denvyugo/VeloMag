window.onload = function () {
     $(".product-list").on("change", "input[id='product-price']", function (event) {
        var target = event.target;
        $.ajax({
            url: "/myadmin/product_price/" + target.name + "/" + target.value + "/",
            success: function (data) {
                $(".product-desc").html(data.result);
            }
        });
    });
    $(".product-list").on("change", "input[id='product-value']", function (event) {
        var target = event.target;
        $.ajax({
            url: "/myadmin/product_value/" + target.name + "/" + target.value + "/",
            success: function (data) {
                $(".product-desc").html(data.result);
            }
        });
    });
}