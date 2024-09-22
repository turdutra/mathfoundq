$(document).ready(function () {
  $('.preloader').fadeOut(100);

  // Function to randomize and filter slides
  function randomizeAndFilterSlides(sliderElement, excludeAlumni = true) {
    var slides = sliderElement.children().toArray();
    slides.sort(function() { return 0.5 - Math.random(); }); // Randomize the array

    slides.forEach(function(slide) {
      var imgSrc = $(slide).find('img').attr('src');
      var category = $(slide).data('category');
      
      // Filter based on category, excluding alumni if excludeAlumni is true
      if (excludeAlumni && !imgSrc.endsWith('alice.png') && !imgSrc.endsWith('bob.png') && category !== 'alumni') {
        sliderElement.append(slide);
      } else if (!excludeAlumni && category === 'alumni') {
        sliderElement.append(slide); // Only include alumni in this case
      } else {
        $(slide).remove();
      }
    });
  }

  // Select the sliders
  var $productSlider = $('.product-slider');
  var $alumniSlider = $('.alumni-slider');

  // Randomize and filter slides
  randomizeAndFilterSlides($productSlider);
  randomizeAndFilterSlides($alumniSlider, false); // Alumni slider should include only alumni

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

  // Initialize alumni slider
  $alumniSlider.slick({
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
