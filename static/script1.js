
// audio_player.js

document.addEventListener('DOMContentLoaded', function () {
    var audio = document.getElementById('audioElement');
    var playButton = document.getElementById('playButton');
    var pauseButton = document.getElementById('pauseButton');

    playButton.addEventListener('click', function () {
        audio.play();
    });

    pauseButton.addEventListener('click', function () {
        audio.pause();
    });
});
