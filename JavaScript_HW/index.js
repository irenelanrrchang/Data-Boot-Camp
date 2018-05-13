// Get references to the tbody element, input field and button
var tbody = document.querySelector("tbody");
var dateInput = document.querySelector("#date");
var cityInput = document.querySelector("#city");
var stateInput = document.querySelector("#state");
var countryInput = document.querySelector("#country");
var shapeInput = document.querySelector("#shape");
var searchBtn = document.querySelector("#search");

// Add an event listener to the searchButton, call handleSearchButtonClick when clicked
searchBtn.addEventListener("click", handleSearchButtonClick);

// Set filteredData to data(Alience) initially
var filteredData = dataSet;

// renderTable renders the filteredData to the tbody
function renderTable() {
  tbody.innerHTML = "";
  for (var i = 0; i < filteredData.length; i++) {
    // Get get the current data(Alience) object and its fields
    var eventData = filteredData[i];
    var fields = Object.keys(eventData);
    // Create a new row in the tbody, set the index to be i + startingIndex
    var row = tbody.insertRow(i);
    for (var j = 0; j < fields.length; j++) {
      // For every field in the data(Alience) object, create a new cell at set its inner text to be the current value at the current data(Alience)'s field
      var field = fields[j];
      var cell = row.insertCell(j);
      cell.innerText = eventData[field];
    }
  }
}

function handleSearchButtonClick() {
  // Format the user's search by removing leading and trailing whitespace, lowercase the string
  var filterDate = dateInput.value.trim();
  var filterCity = cityInput.value.trim().toLowerCase();
  var filterState = stateInput.value.trim().toLowerCase();
  var filterCountry = countryInput.value.trim().toLowerCase();
  var filterShape = shapeInput.value.trim().toLowerCase();

  // Set filteredData to an array of all eventData whose "datetime" matches the filter
  // filteredData = dataSet.filter(function(eventData) {
  //   var eventDataDate = eventData.datetime;

// var eventDataDate = eventData.datetime.toLowerCase();
  function multipleFilter(filteredData) {
      var filtered= [];
      for (var k = 0; k < dataSet.length; k++) {
      var item = dataSet[k];
      // If true, push the data to the filteredlist, otherwise don't add it to filteredlist
      if (item.datetime == filterDate && item.city == filterCity && item.state == filterState  && item.country == filterCountry && item.shape == filterShape) filtered.push(item);
      };

    console.log(filtered)
    
    return filtered;
  }
  
  filtered = multipleFilter(filteredData);  

  renderTable();  
  };


// Render the table for the first time on page load

