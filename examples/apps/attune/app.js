const toast = document.querySelector('#toast');
const pauseButton = document.querySelector('#pauseButton');
const muteButton = document.querySelector('#muteButton');
const endButton = document.querySelector('#endButton');
let toastTimer;

function notify(message) {
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2200);
}

pauseButton.addEventListener('click', () => {
  const paused = document.body.classList.toggle('paused');
  pauseButton.setAttribute('aria-label', paused ? 'Resume listening' : 'Pause listening');
  document.querySelector('.listening-state strong').textContent = paused ? 'Listening paused' : 'Listening together';
  notify(paused ? 'Session paused. Take the time you need.' : 'Listening resumed.');
});

muteButton.addEventListener('click', () => {
  const muted = muteButton.classList.toggle('muted');
  muteButton.setAttribute('aria-label', muted ? 'Unmute microphone' : 'Mute microphone');
  notify(muted ? 'Microphone muted.' : 'Microphone is listening.');
});

endButton.addEventListener('click', () => notify('Session summary is ready when you are.'));
document.querySelector('.try-button').addEventListener('click', () => notify('Take a breath—then say it in your own words.'));
document.querySelector('.another-button').addEventListener('click', () => notify('Another reflection is on its way.'));
document.querySelector('.dismiss').addEventListener('click', (event) => event.currentTarget.closest('.coach-card').remove());
