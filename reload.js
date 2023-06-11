document.addEventListener('DOMContentLoaded', function() {
  // Get all the Pokémon divs
  const pokemonDivs = Array.from(document.querySelectorAll('.pokemon'));

  // Set the initial active index
  let activeIndex = 0;
  pokemonDivs[activeIndex].classList.add('active');

  function showPokemon(index) {
    pokemonDivs[index].classList.add("active");
  }

  function hidePokemon(index) {
    pokemonDivs[index].classList.remove("active");
    pokemonDivs[index].classList.add("hidden");
  }

  const previousButton = document.getElementById('previous-button');
  const nextButton = document.getElementById('next-button');

  previousButton.addEventListener("click", function() {
    hidePokemon(activeIndex);
    activeIndex = (activeIndex - 1 + pokemonDivs.length) % pokemonDivs.length;
    showPokemon(activeIndex);
  });

  nextButton.addEventListener("click", function() {
    hidePokemon(activeIndex);
    activeIndex = (activeIndex + 1) % pokemonDivs.length;
    showPokemon(activeIndex);
  });

  loadImages(); // Call the loadImages function after page load

  setInterval(updateSource, 5000);

  function updateSource() {
    previousButton.disabled = true; // Disable previous button
    nextButton.disabled = true; // Disable next button
    var xhttp = new XMLHttpRequest();
    var uniqueParam = Date.now();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var parser = new DOMParser();
        var responseDoc = parser.parseFromString(this.responseText, 'text/html');
        var partyContent = responseDoc.getElementById('party').innerHTML;
        document.getElementById('party').innerHTML = partyContent;
        loadImages(); // Call the loadImages function after updating the source
        previousButton.disabled = false;
        nextButton.disabled = false;
      }
    };
    xhttp.open("GET", "tracker.html?refresh=" + uniqueParam, true);
    xhttp.send();
  }

  function loadImages() {
    var images = document.querySelectorAll('img[data-src]');
    images.forEach(function(img) {
      var src = img.getAttribute('data-src');
      img.onload = function() {
        img.setAttribute('src', src);
        img.style.opacity = '1';
      };
      img.setAttribute('src', src);
    });
  }
});
