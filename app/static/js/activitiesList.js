function addActivity() {
  const input = document.getElementById('activity');
  const activity = input.value.trim();

  if (activity === '') return;

  const selectedActivities = document.getElementById('selected-activities');

  const activityDiv = document.createElement('div');
  activityDiv.className = 'selected-activity';
  activityDiv.textContent = activity;

  const removeSpan = document.createElement('span');
  removeSpan.className = 'remove-activity';
  removeSpan.textContent = '✖';

  removeSpan.onclick = function() {
    selectedActivities.removeChild(activityDiv);
    updateSelectedActivitiesInput(); // Llama a la función para actualizar el campo oculto
  };

  activityDiv.appendChild(removeSpan);
  selectedActivities.appendChild(activityDiv);
  updateSelectedActivitiesInput(); // Llama a la función para actualizar el campo oculto

  input.value = '';
}

// Función para actualizar el campo oculto con las actividades seleccionadas
function updateSelectedActivitiesInput() {
  const selectedActivitiesDivs = document.querySelectorAll('.selected-activity');
  const selectedActivities = Array.from(selectedActivitiesDivs).map(div => div.textContent);

  const selectedActivitiesInput = document.getElementById('selected_activities_input');
  selectedActivitiesInput.value = JSON.stringify(selectedActivities);
}

function removeActivity(spanElement) {
  const activityDiv = spanElement.parentNode;
  activityDiv.parentNode.removeChild(activityDiv);
  updateSelectedActivitiesInput(); // Llama a la función para actualizar el campo oculto
}

// when enter key is pressed the activity is submited
var input = document.getElementById('activity');
input.addEventListener('keypress', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault();
    document.getElementById('add-activity').click();
  }
});
