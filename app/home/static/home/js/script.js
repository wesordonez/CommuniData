/**
 * This script initializes the functionality for a collapsible button that toggles the visibility of content.
 * It adds a click event listener to the collapsible button and handles the toggling of the content's visibility.
 */
/**
 * Initializes the script when the DOM content is loaded.
 * Adds a click event listener to the collapsible button and toggles the visibility of the content.
 */


// Collapsible button for reviews/partners section

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
  

// Login Modal

var modal = document.getElementById('loginModal');
var btns = document.getElementsByClassName("login-button");
var span = document.getElementsByClassName("close")[0];

for (var i = 0; i < btns.length; i++) {
    btns[i].onclick = function() {
        modal.style.display = "block";
    }
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Smooth scroll to next section
document.addEventListener('DOMContentLoaded', function() {
  const links = document.querySelectorAll('a[href^="#"]');

  for (const link of links) {
      link.addEventListener('click', function(event) {
          event.preventDefault();

          const targetId = this.getAttribute('href').substring(1);
          const targetElement = document.getElementById(targetId);

          if (targetElement) {
              window.scrollTo({
                  top: targetElement.offsetTop,
                  behavior: 'smooth'
              });
          }
      });
  }
});
