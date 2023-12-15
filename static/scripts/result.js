// result.js
document.addEventListener('DOMContentLoaded', function () {
    // Display loading icon
    document.getElementById('loading-icon').style.display = 'block';

    // Simulate a delay (you can replace this with your actual logic)
    setTimeout(function () {
        // Replace this with your actual logic to fetch and display results
        // For now, we're using placeholders
        displayResults('Plant Disease', 'Remedy Information', 'path/to/product_image.jpg');
    }, 3000); // Simulating a 3-second delay, replace with actual delay

    // Function to display results
    function displayResults(predictedDisease, remedyInfo, productImage) {
        // Hide loading icon
        document.getElementById('loading-icon').style.display = 'none';

        // Display the result content
        document.getElementById('result-content').style.display = 'block';

        // Update result information
        document.getElementById('predicted-disease').textContent = predictedDisease;
        document.getElementById('remedy').textContent = remedyInfo;
        document.getElementById('product-image').src = productImage;
    }
});
