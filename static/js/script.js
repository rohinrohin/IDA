$(document).ready(function () {

  $(".team-title").hover(
      function () {
        $("#circular1").removeClass("blur");
        $("#circular2").removeClass("blur");
        $("#circular3").removeClass("blur");
        $("#p1").animate({ opacity: 0 }, 100);
        $("#p2").animate({ opacity: 0 }, 100);;
        $("#p3").animate({ opacity: 0 }, 100);
        $("#p1").hide();
        $("#p2").hide();
        $("#p3").hide();
        $(".about-info").animate({ opacity: 1 }, 150);
      });




    $("#circular1").delay(1000).animate({ opacity: 1 }, 700);
    $("#circular2").delay(1500).animate({ opacity: 1 }, 700);
    $("#circular3").delay(2000).animate({ opacity: 1 }, 700);
    $("#circular1").hover(
        function () {
            $(".about-info").animate({ opacity: 0 }, 150);
            $("#p1").show();
            $("#circular1").removeClass("blur");
            $("#p1").delay(500).animate({ opacity: 1});
            $("#p2").hide();
            $("#p3").hide();
            $("#circular3").addClass("blur");
            $("#circular2").addClass("blur");

        });
    $("#circular2").hover(
        function () {
            $(".about-info").animate({ opacity: 0 }, 150);
            $("#p2").show();
            $("#circular2").removeClass("blur");
            $("#p2").delay(500).animate({ opacity: 1 });
            $("#p1").hide();
            $("#p3").hide();
            $("#circular1").addClass("blur");
            $("#circular3").addClass("blur");
        });
    $("#circular3").hover(
        function () {
            $(".about-info").animate({ opacity: 0 }, 150);
            $("#p3").show();
            $("#circular3").removeClass("blur");
            $("#p3").delay(500).animate({ opacity: 1 });
            $("#p2").hide();
            $("#p1").hide();
            $("#circular1").addClass("blur");
            $("#circular2").addClass("blur");
        });

});


/* Set the width of the side navigation to 250px and the left margin of the page content to 250px and add a black background color to body */

var toggleState = 0; // 0-close 1-open

function openNav() {
    document.getElementById("sideNav").style.width = "150px";
    document.getElementById("main").style.marginLeft = "150px";
    // document.getElementById("video-overlay2").style.opacity = "0.7";
    document.getElementById("about-allwrap").style.opacity = "0.6";
    toggleState = 1;

}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0, and the background color of body to white */
function closeNav() {
    document.getElementById("sideNav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    // document.querySelector("video").style.filter = "blur(0px)";
    // document.getElementById("video-overlay2").style.opacity = "0.5";
    document.getElementById("about-allwrap").style.opacity = "1";
    toggleState = 0;

}

function toggleNav() {
  if (!toggleState)
    openNav();
  else
    closeNav();
}
