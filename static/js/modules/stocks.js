function loadstock() {

  console.log("stocks working");
  var qt = $(".qt");
  console.log(qt.length);

  var spinner = $(".spinner-border");
  spinner.hide();

  var spin = $(".spin");
 
  qt.each(function (index) {
    if ($(this).text() == 0) {
      console.log($(this).text());
      $(this).parent("tr").find("a").hide();
    }
  });

  spin.click(function () {
    console.log("test spin");
    spinner.show();
    $("body").addClass("loading");
  });

}

export { loadstock };
