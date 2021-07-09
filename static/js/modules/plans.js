function loadplan() {


    console.log('plan working');

    var spinner = $(".spinner-border");
    spinner.hide();

    var pl = $(".plan-class");

    pl.click(function (e) {
        e.preventDefault();
        let id = $(this).attr("data-id");
        let url = $(this).attr("data-url");
        let ofi = $(this).attr("data-ofi");
        let quantity = $("#" + id).val();
        console.log(id, ofi, quantity);

        spinner.show();
        $("body").addClass("loading");

        $.ajax({
            url: url,
            data: {
                'id': id,
                'ofi': ofi,
                'quantity': quantity,
            },
            success: (data) => {
                console.log(data);
                spinner.hide();
                $("body").removeClass("loading");
                $(location).attr('href', `/get_stocks/${ofi}`);

            }
        })
    });

}

export { loadplan };