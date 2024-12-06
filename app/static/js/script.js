// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const fieldInput = document.getElementById('field-input');
    const executeBtn = document.getElementById('execute-btn');
    const resultTextarea = document.getElementById('result-textarea');

    browseBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const content = event.target.result;
                resultTextarea.value = content;
            };
            reader.readAsText(file);
        }
    });

    executeBtn.addEventListener('click', () => {
        const fieldName = fieldInput.value.trim();
        if (fieldName) {
            fetch('/Sum_json', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ field_name: fieldName })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status_code === 200) {
                    resultTextarea.value = JSON.stringify(data.data, null, 2);
                } else {
                    resultTextarea.value = `Error: ${data.error}`;
                }
            })
            .catch(error => {
                resultTextarea.value = `Error: ${error.message}`;
            });
        }
    });
});