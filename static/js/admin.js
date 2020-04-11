$(document).ready(function () {
    $('button[name="admin-logout"]').click(() => {
    location.href ='/admin-logout';
    });
    document.getElementsByClassName('admin-singup')[0].addEventListener('click', ()=>{
        location.href ='/admin-registration';
    });
    $('.tabs-item').click(function (e) { 
        e.preventDefault();
        console.log($(this).attr('href'))
        $('.active').removeClass('active')
        $('.visible').removeClass('visible');
        $($(this).attr('href')).toggleClass('visible');
        $(this).toggleClass('active');
    });
        $('.cancel-reg').click(function (e) { 
            e.preventDefault();
            location.href ='/admin';
    });
})