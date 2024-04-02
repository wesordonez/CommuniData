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
  