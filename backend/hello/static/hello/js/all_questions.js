var canHide = true;
const hideQuestionsButton = document.querySelector('input[type=button]');

hideQuestionsButton.addEventListener('click', (ev) => {
    var correctQuestions = document.querySelectorAll('div.question:not(.wrong, .answer)');
    if(canHide) {
        canHide = false;
        correctQuestions.forEach(ele => {
            ele.style.display = 'none';
        })
    } else {
        canHide = true;
        correctQuestions.forEach(ele => {
            ele.style.display = 'block';
        })
    }
})