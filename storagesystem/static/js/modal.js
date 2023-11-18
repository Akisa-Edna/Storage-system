/*function submitForm(formId) {
    console.log('Form submitted!');
    var form = document.getElementById(formId);
    var formData = new FormData(form);

    fetch(form.action, {
         method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
   .then(data => {
      // Handle success
      showBookingConfirmationModal();
   })
   .catch(error => {
      console.error('Error submitting the form:', error);
   });
}
document.getElementById('sharedSpacesSubmitBtn').addEventListener('click', function (event) {
    //event.preventDefault();
    $('#bookingConfirmationModal').modal('show');
    submitForm('sharedSpacesForm'); 
}); */


/*function submitForm(formId) {
    var form = document.getElementById(formId);
    var formData = new FormData(form);

    return fetch(form.action, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(); // Assuming the server returns JSON
    })
    .then(data => {
        // Handle success
        // You can choose to handle the response data here if needed
        // For example, you can check if the response indicates success before showing the modal
        showBookingConfirmationModal();
    })
    .catch(error => {
        console.error('Error submitting the form:', error);
    });
}

// Event listener for the submit button
document.getElementById('sharedSpacesSubmitBtn').addEventListener('click', function (event) {
    // Prevent the default form submission
    event.preventDefault();

    // Submit the form using the submitForm function
    submitForm('sharedSpacesForm')
        .then(() => {
            // Show the booking confirmation modal
            $('#bookingConfirmationModal').modal('show');
        });
});

// Function to display booking details in the modal
function displayBookingDetails(data) {
    // Assuming you have a div with id 'bookingDetails' to display the details
    var bookingDetailsContainer = document.getElementById('bookingDetails');
    
    // Clear previous content
    bookingDetailsContainer.innerHTML = '';

    // Add new content based on the response data
    var bookingSummary = document.createElement('div');
    bookingSummary.innerHTML = `
        <h3 class="pb-3">Booking Summary:</h3>
        <p>${data.spaces[0].name} <span class="pl-3">${data.spaces[0].price}</span></p>
        <p class="font-weight-bold pt-4">Total: ${data.price}</p>
    `;

    // Append the content to the container
    bookingDetailsContainer.appendChild(bookingSummary);
}  */

/*function submitForm(formId) {
    var form = document.getElementById(formId);
    var formData = new FormData(form);

    return fetch(form.action, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Handle success
        console.log('Form submitted successfully!');
        showBookingConfirmationModal(data);
    })
    .catch(error => {
        console.error('Error submitting the form:', error);
    });
}

function showBookingConfirmationModal(data) {
    // Assuming you have a div with id 'bookingDetails' to display the details
    var bookingDetailsContainer = document.getElementById('bookingDetails');
    
    // Clear previous content
    bookingDetailsContainer.innerHTML = '';

    if ('error' in data) {
        // Display an error message if the response indicates an error
        bookingDetailsContainer.innerHTML = `<p>Error: ${data.error}</p>`;
    } else {
        // Add new content based on the response data
        var bookingSummary = document.createElement('div');
        bookingSummary.innerHTML = `
            <h3 class="pb-3">Booking Summary:</h3>
            ${data.spaces.map(space => `<p>${space.name} <span class="pl-3">${space.price}</span></p>`).join('')}
            <p class="font-weight-bold pt-4">Total: ${data.price}</p>
        `;

        // Append the content to the container
        bookingDetailsContainer.appendChild(bookingSummary);

        // Show the booking confirmation modal
        $('#bookingConfirmationModal').modal('show');
    }
}

// Event listener for the submit button
document.getElementById('sharedSpacesSubmitBtn').addEventListener('click', function (event) {
    // Prevent the default form submission
    event.preventDefault();

    console.log('Submit button clicked!');

    // Submit the form using the submitForm function
    submitForm('sharedSpacesForm');
});   */
