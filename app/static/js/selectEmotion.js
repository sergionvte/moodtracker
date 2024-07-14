function selectEmotion(imgElement) {
  const images = document.querySelectorAll('.gallery img');
  images.forEach(img => img.classList.remove('selected'));
  imgElement.classList.add('selected');
  const value = imgElement.getAttribute('data-value');
  console.log(value);
  document.getElementById('selected_value').value = value;
}
