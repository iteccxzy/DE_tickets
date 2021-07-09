function loadcustomer() {
  console.log("customer working2");

  var customer = $("#customer");
  var url1 = customer.attr("data-url1");

  var order = $("#order");

  var id_customer = $("#id_customer");
  var id_office = $("#id_office");
  var odate = $("#id_odate");
  var otime = $("#id_otime");
  var dorder = $("#div-order");
  var oo = order.attr("data-oo");
  var oid = order.attr("data-oid");

  var url_date = order.attr("data-url2");
  var url_time = order.attr("data-url3");
  var url_cus = order.attr("data-url4");

  id_customer.prop("disabled", true);
  id_office.prop("disabled", true);

  var availableFecha = [];
  var availableId = [];

  var spinner = $(".spinner-border");
  spinner.hide();

  // set customer step 1 /////////////////////////////////////////

  customer.submit((event) => {
    event.preventDefault();
 
    let email = $("input[name='email']").val();
    id_customer.val(email);
    id_office.val(oo);
    populate();
    spinner.show();
    $("body").addClass("loading");
  });

  // step 2 /////////////////////////////////////////
  function populate() {
    $.ajax({
      url: url_date,
      data: {
        ofi: oid,
      },
      success: (data) => {
        $.each($(data), (index, value) => {
          availableFecha[index] = moment(value.fields.st_date).format(
            "DD-MM-YYYY"
          );
          availableId[index] = value.pk;
        });
        initComponent(availableFecha);
      },
    }).then(() => {
      dorder.css("display", "flex");
      $("#inp").prop("disabled", true);
    });

    if (odate.val() == "") {
      otime.prop("disabled", true);
    } else {
      otime.prop("disabled", false);
    }
  }

  // step 3 /////////////////////////////////////////
  function initComponent(availableFecha) {
    $("#id_odate").datepicker({
      dateFormat: "yy-mm-dd",
      beforeShowDay: function (d) {
        var mes = d.getMonth() + 1;
        var dia = d.getDate();
        if (mes < 10) {
          mes = "0" + mes;
        }
        if (dia < 10) {
          dia = "0" + dia;
        }
        var dmy = dia + "-" + mes + "-" + d.getFullYear();
        if ($.inArray(dmy, availableFecha) != -1) {
          return [true, "", "Available"];
        } else {
          return [false, "", "unAvailable"];
        }
      },
    });
    spinner.hide();
    $("body").removeClass("loading");
  }

  // step 4 /////////////////////////////////////////
  odate.change(function () {
    let current = $("#id_odate").datepicker("getDate");
    current = moment(current).format("DD-MM-YYYY");
    let indexTime = availableFecha.indexOf(current);
    fetchTime(availableId[indexTime]);
    spinner.show();
    $("body").addClass("loading");
  });

  // step 5 /////////////////////////////////////////
  function fetchTime(st_id) {
    if (odate.val() == "") {
      otime.empty();
      otime.prop("disabled", true);
    } else {
      $.ajax({
        url: url_time,
        data: {
          st_id: st_id,
        },
        success: function (data) {
          otime.prop("disabled", false);
          otime.html(data);
          spinner.hide();
          $("body").removeClass("loading");
        },
      });
    }
  }

  otime.change(() => {
    if (otime.val() == "") {
      $("#inp").prop("disabled", true);
    } else {
      $("#inp").prop("disabled", false);
    }
  });

  // step 6 send form /////////////////////////////////////////
  order.submit((event) => {
    event.preventDefault();
    let name = $("input[name='name']").val();
    let email = $("input[name='email']").val();
    spinner.show();
    $("body").addClass("loading");
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrftoken },
      url: url1,
      data: {
        name: name,
        email: email,
      },
      success: (data) => {
        console.log(data);
      },
    }).then(
      function () {
        let dat = odate.val();
        let tim = otime.val();
        let cus = id_customer.val();
        $.ajax({
          type: "POST",
          headers: { "X-CSRFToken": csrftoken },
          url: url_cus,
          data: {
            office: oid,
            dat: dat,
            tim: tim,
            cus: cus,
          },
          success: function (data) {
            console.log(data);
            spinner.hide();
            $("body").removeClass("loading");
            window.location.href = document.location.href = "/customer";
          },
        });
      },
      function () {
        console.log("no guardado");
      }
    );
  });

  // for csrf
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie("csrftoken");
}

export { loadcustomer };
