const navToggle = document.querySelector('[data-nav-toggle]');
const navLinks = document.querySelector('[data-nav-links]');

if (navToggle && navLinks) {
  const closeNav = () => {
    navLinks.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
  };

  navToggle.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  navLinks.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeNav);
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) closeNav();
  });
}

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!reducedMotion) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add('in');
      });
    },
    { threshold: 0.15 }
  );

  document.querySelectorAll('.fade-up').forEach((el) => observer.observe(el));
} else {
  document.querySelectorAll('.fade-up').forEach((el) => el.classList.add('in'));
  const heroVideo = document.querySelector('.hero video');
  if (heroVideo) heroVideo.pause();
}

const yearTarget = document.querySelector('[data-year]');
if (yearTarget) yearTarget.textContent = new Date().getFullYear();
