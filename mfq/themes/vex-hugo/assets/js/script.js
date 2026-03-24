$(document).ready(function () {
  $('.preloader').fadeOut(100);

  var $meetUsSlider = $('#meet-us-slider');
  var $mfqWorldSlider = $('#mfq-world-slider');
  var sliderOptions = {
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: true,
    dots: false,
    arrows: false,
    swipeToSlide: true,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 2
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1
        }
      }
    ]
  };

  // Function to shuffle items within a container
  function shuffleItems($container) {
    var items = $container.children();
    for (var i = items.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      items.eq(i).before(items.eq(j));
    }
  }

  function pauseSlider($slider) {
    if ($slider.hasClass('slick-initialized')) {
      $slider.slick('slickPause');
    }
  }

  function playSlider($slider) {
    if ($slider.hasClass('slick-initialized')) {
      $slider.slick('slickPlay');
    }
  }

  function bindAutoResume($slider) {
    $slider.on('swipe', function () {
      playSlider($slider);
    });
  }

  function showSlider($sliderToShow, $sliderToHide) {
    $sliderToHide.css('display', 'none');
    pauseSlider($sliderToHide);

    $sliderToShow.css('display', 'block');
    $sliderToShow.slick('setPosition');
    playSlider($sliderToShow);
  }

  // Randomize the sliders once when the page loads
  shuffleItems($meetUsSlider);
  shuffleItems($mfqWorldSlider);

  // Initialize both sliders on page load
  $meetUsSlider.slick(sliderOptions);
  $mfqWorldSlider.slick(sliderOptions);

  bindAutoResume($meetUsSlider);
  bindAutoResume($mfqWorldSlider);
  pauseSlider($mfqWorldSlider);

  // Click event for "Meet Us" link
  $('#meet-us-link').on('click', function () {
    showSlider($meetUsSlider, $mfqWorldSlider);

    // Update text link states
    $('#meet-us-link').removeClass('faded').addClass('active');
    $('#mfq-world-link').removeClass('active').addClass('faded');
  });

  // Click event for "MFQ Around the World" link
  $('#mfq-world-link').on('click', function () {
    showSlider($mfqWorldSlider, $meetUsSlider);

    // Update text link states
    $('#mfq-world-link').removeClass('faded').addClass('active');
    $('#meet-us-link').removeClass('active').addClass('faded');
  });
});
