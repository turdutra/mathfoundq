function preloadImages(array) {
  if (!preloadImages.list) {
    preloadImages.list = [];
  }
  var list = preloadImages.list;
  for (var i = 0; i < array.length; i++) {
    var img = new Image();
    img.src = array[i];
    list.push(img);
  }
}

$(document).ready(function () {
  $('.preloader').fadeOut(100);

  var $meetUsSlider = $('#meet-us-slider');
  var $mfqWorldSlider = $('#mfq-world-slider');

  // Initialize the "Meet Us" slider (Visible by default)
  $meetUsSlider.slick({
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: true,
    dots: false,
    arrows: false,
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
  });

  // Initialize the "MFQ Around the World" slider (Hidden by default)
  $mfqWorldSlider.slick({
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: true,
    dots: false,
    arrows: false,
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
  });

  // Initially hide the MFQ World slider
  $mfqWorldSlider.hide();

  // Click event for "Meet Us" link
  $('#meet-us-link').on('click', function () {
    // Show the Meet Us slider and hide the MFQ Around the World slider
    $mfqWorldSlider.hide();
    $meetUsSlider.show();

    // Update text link states
    $('#meet-us-link').removeClass('faded').addClass('active');
    $('#mfq-world-link').removeClass('active').addClass('faded');
  });

  // Click event for "MFQ Around the World" link
  $('#mfq-world-link').on('click', function () {
    // Show the MFQ Around the World slider and hide the Meet Us slider
    $meetUsSlider.hide();
    $mfqWorldSlider.show();

    // Update text link states
    $('#mfq-world-link').removeClass('faded').addClass('active');
    $('#meet-us-link').removeClass('active').addClass('faded');
  });

  var imageUrls = [];

  $('#meet-us-slider img').each(function () {
    imageUrls.push($(this).attr('src'));
  });

  $('#mfq-world-slider img').each(function () {
    imageUrls.push($(this).attr('src'));
  });

  // Preload all images
  preloadImages(imageUrls);
});