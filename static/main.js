// main.js
document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');

    // Prompt user for camera access
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(error => {
            console.error('Error accessing camera:', error);
        });
});
