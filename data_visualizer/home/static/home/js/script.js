/**
 * This script initializes the functionality for a collapsible button that toggles the visibility of content.
 * It adds a click event listener to the collapsible button and handles the toggling of the content's visibility.
 */
/**
 * Initializes the script when the DOM content is loaded.
 * Adds a click event listener to the collapsible button and toggles the visibility of the content.
 */


document.addEventListener('DOMContentLoaded', (event) => {
    const collapsible = document.querySelector('.collapsible-button');
    const content = document.querySelector('.content');
  
    collapsible.addEventListener('click', function() {
      this.classList.toggle('active');
      if (content.style.display === "block") {
        content.style.display = "none";
      } else {
        content.style.display = "block";
      }
    });
  });
  

// Get the modal
var modal = document.getElementById('loginModal');

// Get the button that opens the modal
var btns = document.getElementsByClassName("login-button");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// Loop over the buttons and add an onclick event listener to each one
for (var i = 0; i < btns.length; i++) {
    btns[i].onclick = function() {
        modal.style.display = "block";
    }
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// function openModal() {
//     modal.style.display = "block";
// }