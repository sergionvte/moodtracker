// Obtener la zona horaria del usuario
const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

// Enviar la zona horaria al servidor junto con la solicitud
fetch('/your-endpoint', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ timezone: timezone, ...otherData }),
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
