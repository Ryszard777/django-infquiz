const nav = document.querySelector('nav');
const hideButton = document.querySelector('button#hide-button');
const hideButtonSVG = document.querySelector('svg#svg-hide-button');
var isHidden = false;

hideButton.addEventListener('click', function() {
  if(isHidden) {
    isHidden = false
  } else {
    isHidden = true
  }
    nav.classList.toggle('hidden');
    if(isHidden)
    {
      hideButton.style.setProperty('transform', `translateY(-${updateNavHeight()}px)`)
    } else {
      hideButton.style.setProperty('transform', 'translateY(0px)')
    }
    document.querySelector('main').classList.toggle('navhidden')
    hideButtonSVG.classList.toggle('rotate-180')
});


function updateNavHeight() {
  const height = nav.offsetHeight;
  document.body.style.setProperty('--nav-height', `-${height}px`);
  return height;
}


updateNavHeight();
window.addEventListener('resize', updateNavHeight);

  function setCookie(cName, cValue, expDays) {
    let date = new Date();
    date.setTime(date.getTime() + (expDays * 24 * 60 * 60 * 1000));
    const expires = "expires=" + date.toUTCString();
    document.cookie = cName + "=" + cValue + "; " + expires + "; path=/";
}
const themeSlider = document.querySelector('input[type=checkbox]#theme-slider')
themeSlider.addEventListener('change', (ev) => {
  if(themeSlider.checked) setCookie('theme', 'dark', 7)
  else setCookie('theme', 'light', 7)
})