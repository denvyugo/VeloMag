window.onload = function () {
    $("#product-value").on("change", "input[type='number']", function (event) {
        var target = event.target;
        $.ajax({
            url: "/myadmin/product_value/" + target.name + "/" + target.value + "/",
            success: function (data) {
                $(".product-desc").html(data.result);
            }
        });
    });
	$("#product-price").on("change", "input[type='number']", function (event) {
        var target = event.target;
        $.ajax({
            url: "/myadmin/product_price/" + target.name + "/" + target.value + "/",
            success: function (data) {
                $(".product-desc").html(data.result);
            }
        });
    });
}