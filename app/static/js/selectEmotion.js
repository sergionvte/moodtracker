function selectEmotion(imgElement) {
  const images = document.querySelectorAll('.gallery img');

  // Verificar si el elemento ya tiene la clase 'selected'
  if (imgElement.classList.contains('selected')) {
    // Si ya está seleccionado, remover la clase 'selected'
    imgElement.classList.remove('selected');
    document.getElementById('selected_value').value = ''; // Resetear el valor seleccionado
  } else {
    // Si no está seleccionado, remover la clase 'selected' de todas las imágenes y agregarla al elemento clicado
    images.forEach(img => img.classList.remove('selected'));
    imgElement.classList.add('selected');
    const value = imgElement.getAttribute('data-value');
    document.getElementById('selected_value').value = value; // Actualizar el valor seleccionado
  }
}
