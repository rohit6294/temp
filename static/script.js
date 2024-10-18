const uploadForm = document.getElementById('uploadForm');
        const resultContainer = document.getElementById('resultContainer');
        const uploadedImage = document.getElementById('uploadedImage');
        const predictionResult = document.getElementById('predictionResult');

        uploadForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(uploadForm);
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            // Display the uploaded image
            uploadedImage.src = URL.createObjectURL(formData.get('file'));
            uploadedImage.style.display = 'block';

            // Display the prediction result
            predictionResult.textContent = data.result;
        });