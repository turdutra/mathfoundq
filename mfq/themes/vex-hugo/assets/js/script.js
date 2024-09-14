$(document).ready(function () {
  $('.preloader').fadeOut(100);

  // Function to randomize slides and remove people without photos and alumni category
  function randomizeAndFilterSlides(sliderElement) {
    var slides = sliderElement.children().toArray();
    slides.sort(function() { return 0.5 - Math.random(); }); // Randomize the array

    // Filter and re-append slides
    slides.forEach(function(slide) {
      // Get the src of the image and the category from data attributes or HTML structure
      var imgSrc = $(slide).find('img').attr('src');
      var category = $(slide).data('category'); // Assuming category is stored in a data attribute
      
      // Check if the image source is neither 'alice.png' nor 'bob.png'
      // and filter out alumni category
      if (!imgSrc.endsWith('alice.png') && !imgSrc.endsWith('bob.png') && category !== 'alumni') {
        sliderElement.append(slide); // Re-append slides in random order if they don't match
      } else {
        $(slide).remove(); // Remove slides with specific images or alumni category
      }
    });
  }

  // Select the slider containers
  var $productImageSlider = $('.product-image-slider');
  var $productSlider = $('.product-slider');

  // Randomize and filter slides
  randomizeAndFilterSlides($productImageSlider);
  randomizeAndFilterSlides($productSlider);

  // Initialize product image slider
  $productImageSlider.slick({
    autoplay: false,
    infinite: true,
    arrows: false,
    dots: true,
    customPaging: function (slider, i) {
      var image = $(slider.$slides[i]).data('image');
      return '<img class="img-fluid" src="' + image + '" alt="product-image">';
    }
  });

  // Initialize product slider
  $productSlider.slick({
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: true,
    dots: false,
    arrows: false,
    responsive: [{
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
});
