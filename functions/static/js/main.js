
function selection_send(){
    document.querySelector('.btn-search').addEventListener('click', function (e) {
        e.preventDefault(); // Prevent form submission
    
        // Get all select elements with the class 'input-select'
        const selects = document.querySelectorAll('.input-select select');
    
        // Create an object to store the selected values
        const selectedValues = {};
    
        // Iterate through each select element
        selects.forEach((select) => {
          const name = select.getAttribute('name') || 'unknown'; // Use the 'name' attribute as the key
          const value = select.value; // Get the selected value
          selectedValues[name] = value; // Store the value in the object
        });
    
        // Log the selected values
        console.log(selectedValues);
    
        // You can send the selectedValues object to the server or use it as needed
      });
}
