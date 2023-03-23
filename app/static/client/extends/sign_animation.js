// add animation for my inputs
function addAnimation() {
    var inputs = document.querySelectorAll('.input');
    inputs.forEach(function (input) {
        input.addEventListener('focus', function () {
            input.classList.add('focus');
        });
        input.addEventListener('blur', function () {
            input.classList.remove('focus');
        });
    });
}