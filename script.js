document.addEventListener("DOMContentLoaded", function () {
    // Fetch dropdown options (areas and items) from the Flask backend
    fetch('http://127.0.0.1:5000/dropdown-options')
        .then(response => response.json())
        .then(data => {
            const cropSelect = document.getElementById('crop');
            const countrySelect = document.getElementById('country');
            
            // Populate crop options
            data.items.forEach(item => {
                const option = document.createElement('option');
                option.value = item;
                option.textContent = item;
                cropSelect.appendChild(option);
            });

            // Populate country options (assuming country corresponds to areas)
            data.areas.forEach(area => {
                const option = document.createElement('option');
                option.value = area;
                option.textContent = area;
                countrySelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching dropdown options:', error);
        });

    // Handle form submission
    const predictionForm = document.getElementById('predictionForm');
    predictionForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from submitting and refreshing the page

        // Get form input values
        const crop = document.getElementById('crop').value;
        const country = document.getElementById('country').value;
        const year = document.getElementById('feature1').value;
        const rainfall = document.getElementById('feature2').value;
        const pesticides = document.getElementById('feature3').value;
        const temperature = document.getElementById('feature4').value;

        // Prepare the data to send to the backend for prediction
        const predictionData = {
            Area: country,
            Item: crop,
            Year: year,
            average_rain_fall_mm_per_year: rainfall,
            pesticides_tonnes: pesticides,
            avg_temp: temperature
        };

        // Send data to the Flask backend for prediction
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(predictionData)
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('result');
            if (data.predicted_percentage) {
                resultDiv.innerHTML = `
                    <h3>Prediction Result:</h3>
                    <p>Predicted Yield: ${data.predicted_percentage.toFixed(2)}%</p>
                `;
            } else {
                resultDiv.innerHTML = `
                    <h3>Error:</h3>
                    <p>${data.error}</p>
                `;
            }
        })
        .catch(error => {
            console.error('Error during prediction:', error);
        });
    });
});
