const toggleBtn = document.querySelector('.navbar__toggleBtn');
const navBarBtn = document.querySelector('.navbar__buttons');

toggleBtn.addEventListener('click', () => {
  navBarBtn.classList.toggle('active');
});