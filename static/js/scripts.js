/*
 * Copyright (c) 2024 LongbowXXX
 *
 * This software is released under the MIT License.
 * http://opensource.org/licenses/mit-license.php
 */

$(document).ready(function () {
    $("#user-input-form").on("submit", function (event) {
        event.preventDefault();
        $.ajax({
            url: "/agent",
            type: "POST",
            data: $(this).serialize(),
            success: function (data) {
                $("#history").append('<li class="user-input"><strong>User:</strong> ' + data.user_input + '</li>');
                $("#history").append('<li class="system-response"><strong>Response:</strong> ' + data.response + '</li>');
                $("#user-input").val('');
                let utterance = new SpeechSynthesisUtterance(data.response);
                window.speechSynthesis.speak(utterance);
            }
        });
    });
});
