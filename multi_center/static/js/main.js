$(function () {
  $(".sidebar_left_title").click(function () {
    $(".sidebar_left_title").removeClass("active");
    $(this).toggleClass("active");
  });
  $(".sidebar_1").click(function () {
    $(".index_main").removeClass("active");
    $(".index_desc_main").addClass("active");
  });
  $(".sidebar_2").click(function () {
    $(".index_main").removeClass("active");
    $(".index_desc_service").addClass("active");
  });
  $(".sidebar_3").click(function () {
    $(".index_main").removeClass("active");
    $(".index_desc_extra").addClass("active");
  });

  $(".modal .close").on("click", function () {
    $(this).closest(".modal").removeClass("show");
  });

  $(".li_left").on("click", function () {
    if ($(this).hasClass("active")) {
      $(this).removeClass("active");
    } else {
      $(".li_left").removeClass("active");
      $(this).addClass("active");
    }
  });
});
