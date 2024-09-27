$(document).ready(function () {
  $('.preloader').fadeOut(100);

  var $meetUsSlider = $('#meet-us-slider');
  var $mfqWorldSlider = $('#mfq-world-slider');

  // Function to shuffle items within a container
  function shuffleItems($container) {
    var items = $container.children();
    for (var i = items.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      items.eq(i).before(items.eq(j));
    }
  }

  // Function to preload images
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

  // Randomize the sliders once when the page loads
  shuffleItems($meetUsSlider);
  shuffleItems($mfqWorldSlider);

  // Initialize both sliders on page load
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

  // Click event for "Meet Us" link
  $('#meet-us-link').on('click', function () {
    // Hide the MFQ Around the World slider
    $mfqWorldSlider.css('display', 'none');
    // Show the Meet Us slider
    $meetUsSlider.css('display', 'block');
    $meetUsSlider.slick('setPosition'); // Recalculate layout

    // Update text link states
    $('#meet-us-link').removeClass('faded').addClass('active');
    $('#mfq-world-link').removeClass('active').addClass('faded');
  });

  // Click event for "MFQ Around the World" link
  $('#mfq-world-link').on('click', function () {
    // Hide the Meet Us slider
    $meetUsSlider.css('display', 'none');
    // Show the MFQ Around the World slider
    $mfqWorldSlider.css('display', 'block');
    $mfqWorldSlider.slick('setPosition'); // Recalculate layout

    // Update text link states
    $('#mfq-world-link').removeClass('faded').addClass('active');
    $('#meet-us-link').removeClass('active').addClass('faded');
  });

  // Preload all slider images
  var imageUrls = [];
  $('#meet-us-slider img').each(function () {
    imageUrls.push($(this).attr('src'));
  });
  $('#mfq-world-slider img').each(function () {
    imageUrls.push($(this).attr('src'));
  });

  // Call the image preloader function
  preloadImages(imageUrls);
});
