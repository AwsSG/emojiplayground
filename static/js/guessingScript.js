let guessForm = document.getElementById('guess-form');
let feedbackContainer = document.getElementById('guess-feedback');
let guessesRemainingContainer = document.getElementById('guesses-remaining');
let waiting = false;
guessForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    let guess = e.target[0].value.toLowerCase().split(" ");;
    let guessesRemaining = parseInt(guessesRemainingContainer.innerText);
    if(!waiting) {
    $.ajax({
            url: "",
            type: "get",
            contentType: "application/json",
            data: {guess: "okey-dokey"},
            success: function(response) {
                waiting=true;
                let answer = response.answer.toLowerCase().split(" ");

                let guessWordsMatched = 0;
                let guessWordsUnmatched = 0;
                let answerWordsMatched = 0;
                let answerWordsUnmatched = 0;

                guess.forEach((guessWord) => {
                    let matched = false;
                    answer.forEach((answerWord) => {
                        if(answerWord === guessWord) {
                            guessWordsMatched += 1;
                            matched = true;
                        }
                    })
                    if (!matched) {
                        guessWordsUnmatched += 1;
                    }
                });
                let answerMatchArray = []

                answer.forEach((answerWord) => {
                    let matched = false;
                    guess.forEach((guessWord) => {
                        if(guessWord === answerWord) {
                            answerWordsMatched += 1;
                            matched = true;
                        }
                    })
                    if (!matched) {
                        answerMatchArray.push(-1);
                        answerWordsUnmatched += 1;
                    }
                    else {
                        answerMatchArray.push(1);
                    }
                });
                answerMatchThreshold = 0;
                answerMatchArray.forEach((val)=>{
                    answerMatchThreshold += val;
                })
                console.log(answerMatchThreshold);

                let totalWords = guessWordsMatched + guessWordsUnmatched +
                    answerWordsMatched + answerWordsUnmatched;
                let correctWords = guessWordsMatched + answerWordsMatched;
                let correctPercentage = correctWords / totalWords;
                console.log(correctPercentage);
                if (correctPercentage >= .9 && answerMatchThreshold > 0) {
                    console.log('correct');
                    feedbackContainer.innerText = `That's Right the answer was "${response.answer}"! Well Done`;
                }
                if (correctPercentage >= .7 && correctPercentage < .9) {
                    feedbackContainer.innerText = "You're almost there! Just a little tweak..."
                    guessesRemaining = guessesRemaining - 1;
                    guessesRemainingContainer.innerText= guessesRemaining;
                }
                else if (correctPercentage < .75 && correctPercentage >= .5) {
                    feedbackContainer.innerText = "Not a bad guess. Try again..."
                    guessesRemaining = guessesRemaining - 1;
                    guessesRemainingContainer.innerText= guessesRemaining;
                }
                else if (correctPercentage < .5) {
                    feedbackContainer.innerText = "Not even close! You'll have to do better than that..."
                    guessesRemaining = guessesRemaining - 1;
                    guessesRemainingContainer.innerText= guessesRemaining;
                }
                else if (correctPercentage >=.9 && answerMatchThreshold <=0 ) {
                    feedbackContainer.innerText = "That's not right. Give it another go..."
                    guessesRemaining = guessesRemaining - 1;
                    guessesRemainingContainer.innerText= guessesRemaining;
                }
                if (guessesRemaining <= 0) {
                    feedbackContainer.innerText = "No guesses Remaining. Try another puzzle"
                }
                else{
                    waiting = false
                };
            }
        })
    }
});