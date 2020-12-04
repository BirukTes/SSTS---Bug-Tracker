$(document).ready(function () {
});

function switchToLogin() {
    $.ajax({
        type: 'GET',
        url: '/login',
        dataType: 'html',
        success: function (data) {
            $("#authentication-card").html(data);
        }
    });
}

function switchToRegister() {
    $.ajax({
        type: 'GET',
        url: '/register',
        dataType: 'html',
        success: function (data) {
            $("#authentication-card").html(data);
        }
    });
}
