window.addEventListener('scroll', function() {
    var navbar = document.querySelector('.navbar');
    var navTexts = document.querySelectorAll('.nav-text'); 

    if (window.scrollY > 80) {
        navbar.style.backgroundColor = '#ffffff';
        navbar.style.boxShadow = '1px 2px 15px rgba(100, 100, 100, 0.3)';
        navTexts.forEach(function(navText) {
            navText.style.color = 'black';
        });
    } else {
        navbar.style.backgroundColor = 'transparent';
        navbar.style.boxShadow = 'none'; 
        navTexts.forEach(function(navText) {
            navText.style.color = 'white';
        });
    }
});

$(document).ready(function(){
    $('.owl-carousel').owlCarousel({
        items: 1, 
        slideBy: 1,
        loop: true,
        margin: 10,
        nav: true, 
        dots: true 
    });
  });
  

