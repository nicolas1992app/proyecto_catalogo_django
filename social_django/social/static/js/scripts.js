"use strict";


   console.log("hola");
    $('#submitBtn').click(function() {
        $('#uname').text($('#username').val());
        $('#psw').text($('#password').val());
    });