//jQuery code
jQuery(function($) {

  "use strict";

  // Preloader
  $(window).on('load', function () {
	setTimeout(delayload, 300);
  });

  $(document).ready(function () {

  initPopup();
  initMail();
  initScroll();
  // initOverlay();
  // initGallery();

  });

});


function delayload  () {
	var $preloader = $('#page-preloader'),
        $spinner   = $preloader.find('.spinner');
    $spinner.fadeOut();
    $preloader.fadeOut('slow');

    $('.header-text').addClass('header-text-animation');
    $('.sub-text').addClass('sub-text-animation');



}








// Notify Popup
function initPopup() {
  $('.notify-popup').magnificPopup({
    type:'inline',
    midClick: true,
    removalDelay: 300,
    mainClass: 'mfp-fade'
  });
}

// Gallery
function initGallery() {
  $('#gallery').magnificPopup({
    delegate: 'a',
    type: 'image',
    removalDelay: 300,
    mainClass: 'mfp-fade-gallery',
    gallery: {
      enabled:true
    }
  });
}

// Email Validate
function validateEmail(email) {
  var reg = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return reg.test(email);
}

// Notify Form Validation
function initMail() {

    $('#form-notify1').submit(function(){

    $("#submit1").replaceWith("<em>Sending...</em>");
    $.ajax({
        url: '/predictrisk',
        type: 'POST',
        data : $('#form-notify1').serialize(),
        success: function (data) {
        if (data == "true") {
            submitted();
        }
    }
    });
    return false;
    });

    $('#form-notify2').submit(function(){

    $("#submit2").replaceWith("<em>Sending...</em>");
    $.ajax({
        url: '/doappoint',
        type: 'POST',
        data : $('#form-notify2').serialize(),
        success: function (data) {
        if (data == "true") {
            submitted();
        }
    }
    });
    return false;
    });



    // $("#form-notify1").submit(function () {
    //     return false;
    // });
    // //
    // $("#submit1").on("click", function () {
    //     var emailval = $("#email").val();
    //     var emailvalid = validateEmail(emailval);
    //     if (emailvalid == false) {
    //         $(".form-error-message").addClass("error");
    //     }
    //     else if (emailvalid == true) {
    //         $(".form-error-message").removeClass("error");
    //     }
    //     if (emailvalid == true) {
    //         alert("going to send");
    //         $("#submit1").replaceWith("<em>Sending...</em>");
    //         $.ajax({
    //             type: 'POST',
    //             url: 'http://requestb.in/rktw6crk',
    //             data: $("#form-notify1").serialize(),
    //             success: function (data) {
    //                 if (data == "true") {
    //                     $("#form-notify1").fadeOut("fast", function () {
    //                         $(this).before("<span class='success'>Message sent</span>");
    //                     });
    //                 }
    //             }
    //         });
    //     }
    // });

    // $("#submit2").on("click", function () {
    //     var emailval = $("#email").val();
    //     var emailvalid = validateEmail(emailval);
    //     if (emailvalid == false) {
    //         $(".form-error-message").addClass("error");
    //     }
    //     else if (emailvalid == true) {
    //         $(".form-error-message").removeClass("error");
    //     }
    //     if (emailvalid == true) {
    //         $("#submit2").replaceWith("<em>Sending...</em>");
    //         // $.ajax({
    //         //     type: 'POST',
    //         //     url: '/predictrisk',
    //         //     data: $("#form-notify2").serialize(),
    //         //     success: function (data) {
    //         //         if (data == "true") {
    //         //             $("#form-notify2").fadeOut("fast", function () {
    //         //                 $(this).before("<span class='success'>Message sent</span>");
    //         //             });
    //         //         }
    //         //     }
    //         // });
    //     }
    // });

}

// Information Window (Read More)
function initOverlay() {
  var container = document.querySelector( 'div.container-animation' ),
    triggerBttn = document.getElementById( 'more-btn' ),
    overlay = document.querySelector( 'div.overlay' ),
    closeBttn = overlay.querySelector( 'button.overlay-close' );
    transEndEventNames = {
      'WebkitTransition': 'webkitTransitionEnd',
      'MozTransition': 'transitionend',
      'OTransition': 'oTransitionEnd',
      'msTransition': 'MSTransitionEnd',
      'transition': 'transitionend'
    },
    transEndEventName = transEndEventNames[ Modernizr.prefixed( 'transition' ) ],
    support = { transitions : Modernizr.csstransitions };

  function toggleOverlay() {
    if( classie.has( overlay, 'open' ) ) {
      classie.remove( overlay, 'open' );
      classie.remove( container, 'overlay-open' );
      classie.add( overlay, 'close' );
      var onEndTransitionFn = function( ev ) {
        if( support.transitions ) {
          if( ev.propertyName !== 'visibility' ) return;
          this.removeEventListener( transEndEventName, onEndTransitionFn );
        }
        classie.remove( overlay, 'close' );
      };
      if( support.transitions ) {
        overlay.addEventListener( transEndEventName, onEndTransitionFn );
      }
      else {
        onEndTransitionFn();
      }
    }
    else if( !classie.has( overlay, 'close' ) ) {
      classie.add( overlay, 'open' );
      classie.add( container, 'overlay-open' );
    }
  }

  triggerBttn.addEventListener( 'click', toggleOverlay );
  closeBttn.addEventListener( 'click', toggleOverlay );
}

// Scroll
function initScroll() {
  $('.nano').nanoScroller({
    preventPageScrolling: true
  });
}

function submitted(){
//    var myNode = document.getElementById("notify1").className+= " newsletter-onsubmit";
    document.querySelector(".newsletter").style.height="300px";     
    document.querySelector(".newsletter").style.maxWidth="750px";
    document.querySelector(".newsletter").style.backgroundColor="green";
    document.querySelector(".newsletter").style.color="white";
    document.querySelector(".newsletter").style.display="flex";
//    document.querySelector(".newsletter").setAttribute("style", "align-items: center");

//    while (myNode.firstChild) {
//        myNode.removeChild(myNode.firstChild);
//    }
    document.querySelector("#notify-wrapper").style.display = "none";  
    document.querySelector("#completed").style.display = "block";

}
