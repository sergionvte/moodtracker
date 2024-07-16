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
  };
  activityDiv.appendChild(removeSpan);
  selectedActivities.appendChild(activityDiv);
  input.value = '';
}

// when enter key is pressed the activity is submited
var input = document.getElementById('activity');
input.addEventListener('keypress', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault();
    document.getElementById('add-activity').click();
  }
});
