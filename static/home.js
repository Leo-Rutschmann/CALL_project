toggleSuggestions = () => {
    let suggestionsContainer = document.getElementById('suggestionContainer');
    suggestionsContainer.classList.toggle('content--hidden');
    document.cookie = 'suggestionsActive=' + ((suggestionsContainer.classList.contains('content--hidden')) ? '1' : '0');
}