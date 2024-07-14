function addActivity() {
  console.log('Hi from activitiesList.js!')
  const input = document.getElementById('activity');
  const activity = input.value.trim();

  if (activity === '') return;

  const selectedActivities = document.getElementById('selected-activities');

  const activityDiv = document.createElement('div');
  activityDiv.className = 'selected-activity';
  activityDiv.textContent = activity;

  const removeSpan = document.createElement('span');
  removeSpan.className = 'remove-activity';
  removeSpan.textContent = 'x';

  removeSpan.onclick = function() {
    selectedActivities.removeChild(activityDiv);
  };
  activityDiv.appendChild(removeSpan);
  selectedActivities.appendChild(activityDiv);
  input.value = '';
}
