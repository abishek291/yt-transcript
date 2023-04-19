const summarizeBtn = document.getElementById('summarize-btn');
const summaryText = document.getElementById('summary-text');

summarizeBtn.addEventListener('click', () => {
    const transcript = document.getElementById('transcript').innerText;
    fetch('/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ transcript })
    })
    .then(response => response.text())
    .then(summary => {
        summaryText.innerText = summary;
    });
});
