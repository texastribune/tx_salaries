var $navPos = $('.over-bar').position().top;
var $nav = $('.over-bar');

$(window).scroll(function() {
  var $scrollTop = $(window).scrollTop();
  $('.active').removeClass('active');
  $fixRail($scrollTop);
  $highlightArrows($scrollTop);
});


var $highlightArrows = function(scrollTop) {
  if (scrollTop > $('#employment').position().top) {
    $('#employment-arrow').addClass('active');
  } else if (scrollTop > $('#ethnicity').position().top) {
    $('#ethnicity-arrow').addClass('active');
  } else if (scrollTop > $('#gender').position().top) {
    $('#gender-arrow').addClass('active');
  } else {
    $('#overview-arrow').addClass('active');
  }
};

var $fixRail = function(scrollTop) {
  if (scrollTop > $navPos) {
    $nav.addClass('fixed-rail');
    $nav.css('width', $('.overview_header').width());
  } else {
    $nav.removeClass('fixed-rail');
  }
};
