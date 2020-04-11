document.getElementsByClassName('login-button')[0].addEventListener('click', ()=>{
    location.href ='/login';
});
$('button[name="login"]').click(function () {
    console.log('logined')
    location.href ='/admin';
});
$('.cancel-log').click(function (e) { 
    e.preventDefault();
    location.href ='/';
});