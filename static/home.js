toggleSuggestions = () => {
    let suggestionsContainer = document.getElementById('suggestionContainer');
    suggestionsContainer.classList.toggle('content--hidden');
    document.cookie = 'suggestionsActive=' + ((suggestionsContainer.classList.contains('content--hidden')) ? '1' : '0');
}

takeAnswer = () => {
    // document.getElementById('proceedButton').classList.remove('content--hidden')
    document.getElementById('revealContainer').classList.remove('content--hidden')
    document.getElementById('proceedButton').classList.remove('content--hidden')
    document.getElementById('questionWrapper').classList.add('content--hidden')
    document.getElementById('guessInputField').classList.add('content--hidden')
    document.getElementById('submitAnswerButton').classList.add('content--hidden')
    document.getElementById('guessLabel').classList.add('content--hidden')
}