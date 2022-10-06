/*Parallax.js init*/
var scene = $("#scene").get(0);
var parallax = new Parallax(scene);

/*Logo Hover*/
$(".main_logo").hover(
    function () {
      $(".back-hexa img:last-child").css("opacity", "0");
      $(".back-hexa img:nth-child(1)").css("opacity", "1");
      $(".descriptor b").css("color", "#fbea2c")
    },
    function () {
      $(".back-hexa img:last-child").css("opacity", "1");
      $(".back-hexa img:nth-child(1)").css("opacity", "0");
      $(".descriptor b").css("color", "white")
    }
  );
