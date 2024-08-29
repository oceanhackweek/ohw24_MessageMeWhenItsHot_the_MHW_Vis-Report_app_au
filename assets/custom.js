$(document).ready(function(){
    $("#contact-link").click(function(){
        $(".contact-container").toggleClass("active");
    });

    $('.animated-dropdown').on('click', function() {
        $(this).addClass('animate__animated animate__pulse shadow-lg');
    });

    $('.animated-dropdown').on('blur', function() {
        $(this).removeClass('animate__animated animate__pulse shadow-lg');
    });
});
