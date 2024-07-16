document.getElementById('sendData').addEventListener('click', function() {
  var elements = document.querySelectorAll('.selected-activity');
  var data = [];
  elements.forEach(function(element) {
    data.push(element.textContent);
  });

  fetch('/process_data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ elements: data })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
});
