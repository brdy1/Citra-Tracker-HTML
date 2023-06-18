// Function to make an XMLHttpRequest to refresh the party content
function refreshPartyContent() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
      var parser = new DOMParser();
      var responseDoc = parser.parseFromString(this.responseText, 'text/html');
      var newPokemonDivs = responseDoc.querySelectorAll("#party .pokemon");
      // Check if activeIndex is still valid
      if (activeIndex >= newPokemonDivs.length) {
        activeIndex = 0; // Reset to 0 if invalid
      }
      setActivePokemon(newPokemonDivs,activeIndex);
      var partyContent = responseDoc.getElementById('party').innerHTML;
      document.getElementById('party').innerHTML = partyContent;
    }
  };
  xhttp.open("GET", "tracker.html", true); // Replace with your server endpoint
  xhttp.send();
  // Initially assign the "hidden" class to all Pokémon divs except the active one

}

// Function to handle button clicks
function handleButtonClick(event) {
  var pokemonDivs = document.querySelectorAll("#party .pokemon");
  
  // Add hidden class to the currently active pokemon div
  pokemonDivs[activeIndex].classList.add("hidden");
  
  if (event.target.id === "previous-button") {
    activeIndex = (activeIndex === 0) ? pokemonDivs.length - 1 : activeIndex - 1;
  } else if (event.target.id === "next-button") {
    activeIndex = (activeIndex === pokemonDivs.length - 1) ? 0 : activeIndex + 1;
  }
  
  // Remove hidden class from the new active pokemon div
  pokemonDivs[activeIndex].classList.remove("hidden");
  setActivePokemon(pokemonDivs,activeIndex);
}

// Function to get the index of the active pokemon div
function getActivePokemonIndex(pokemonDivs) {
  for (var i = 0; i < pokemonDivs.length; i++) {
    if (!pokemonDivs[i].classList.contains("hidden")) {
      return i;
    }
  }
  return 0; // Return 0 if no active pokemon found
}

// Set initial active index from memory (or default to 0)
var activeIndex = parseInt(localStorage.getItem("activeIndex")) || 0;
var pokemonDivs = document.querySelectorAll("#party .pokemon");
setActivePokemon(pokemonDivs,activeIndex);

// Add event listeners to buttons
document.getElementById("previous-button").addEventListener("click", handleButtonClick);
document.getElementById("next-button").addEventListener("click", handleButtonClick);

// Function to set the active pokemon based on the index
function setActivePokemon(divs,activeIndex) {
  for (var i = 0; i < divs.length; i++) {
    if (i === activeIndex) {
      divs[i].classList.remove("hidden");
    } else {
      divs[i].classList.add("hidden");
    }
  }
  localStorage.setItem("activeIndex", activeIndex); // Store active index in memory
}

// Refresh party content every 5 seconds (5000 milliseconds)
setInterval(refreshPartyContent, 10000);
// Initially assign the "hidden" class to all Pokémon divs except the active one
for (var i = 0; i < pokemonDivs.length; i++) {
  if (i !== activeIndex) {
    pokemonDivs[i].classList.add("hidden");
  }
}

//   function loadImages() {
//     var images = document.querySelectorAll('img[data-src]');
//     images.forEach(function(img) {
//       var src = img.getAttribute('data-src');
//       img.onload = function() {
//         img.setAttribute('src', src);
//         img.style.opacity = '1';
//       };
//       img.setAttribute('src', src);
//     });
//   }

// document.addEventListener('DOMContentLoaded', function() {
//   // Get all the Pokémon divs
//   const pokemonDivs = Array.from(document.querySelectorAll('.pokemon'));

//   // Set the initial active index
//   let activeIndex = 0;
//   pokemonDivs[activeIndex].classList.add('active');

//   function showPokemon(index) {
//     pokemonDivs[index].classList.add("active");
//   }

//   function hidePokemon(index) {
//     pokemonDivs[index].classList.remove("active");
//     pokemonDivs[index].classList.add("hidden");
//   }

//   const previousButton = document.getElementById('previous-button');
//   const nextButton = document.getElementById('next-button');

//   previousButton.addEventListener("click", function() {
//     hidePokemon(activeIndex);
//     activeIndex = (activeIndex - 1 + pokemonDivs.length) % pokemonDivs.length;
//     showPokemon(activeIndex);
//   });

//   nextButton.addEventListener("click", function() {
//     hidePokemon(activeIndex);
//     activeIndex = (activeIndex + 1) % pokemonDivs.length;
//     showPokemon(activeIndex);
//   });

//   loadImages(); // Call the loadImages function after page load

//   setInterval(updateSource, 5000);

//   function updateSource() {
//     previousButton.disabled = true; // Disable previous button
//     nextButton.disabled = true; // Disable next button
//     var xhttp = new XMLHttpRequest();
//     var uniqueParam = Date.now();
//     xhttp.onreadystatechange = function() {
//       if (this.readyState == 4 && this.status == 200) {
//         var parser = new DOMParser();
//         var responseDoc = parser.parseFromString(this.responseText, 'text/html');
//         var partyContent = responseDoc.getElementById('party').innerHTML;
//         document.getElementById('party').innerHTML = partyContent;
//         loadImages(); // Call the loadImages function after updating the source
//         previousButton.disabled = false;
//         nextButton.disabled = false;
//       }
//     };
//     xhttp.open("GET", "tracker.html?refresh=" + uniqueParam, true);
//     xhttp.send();
//   }

//   function loadImages() {
//     var images = document.querySelectorAll('img[data-src]');
//     images.forEach(function(img) {
//       var src = img.getAttribute('data-src');
//       img.onload = function() {
//         img.setAttribute('src', src);
//         img.style.opacity = '1';
//       };
//       img.setAttribute('src', src);
//     });
//   }
// });
