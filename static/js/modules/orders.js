function loadorder() {
   
    console.log('orders working');
    var dl = $('.delete1');
    var mm =''

    var spinner = $(".spinner-border");
    spinner.hide();

    dl.click(function (evt) {
        mm = this.getAttribute('data-order');
        console.log('im here', mm);
        evt.preventDefault();
        $('#exampleModal').modal('show');

    });
    $('#accept').click(() => {

        spinner.show();
    $("body").addClass("loading");

        $(location).attr('href', `/delete_order/${mm}`);
        console.log(mm, "order");
        $('#exampleModal').modal('hide');
    });

}

export {loadorder};


