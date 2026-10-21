// ===== Rose 73 — интерактив =====

// --- мобильное меню ---
const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');

if (menuToggle && nav) {
  menuToggle.addEventListener('click', () => {
    const open = menuToggle.getAttribute('aria-expanded') === 'true';
    menuToggle.setAttribute('aria-expanded', String(!open));
    nav.classList.toggle('mobile-open', !open);
  });

  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      menuToggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('mobile-open');
    });
  });
}

// --- бегущая строка: добираем копии, чтобы не было пустот на широких экранах ---
const marquee = document.querySelector('.marquee-track');
if (marquee) {
  let guard = 0;
  while (marquee.scrollWidth < window.innerWidth * 2.2 && guard < 4) {
    marquee.innerHTML += marquee.innerHTML; // чётное число копий → шов совпадает
    guard++;
  }
}

// --- плавное появление блоков при прокрутке ---
const revealTargets = document.querySelectorAll(
  '.section-head, .occasions, .about-copy, .features, .steps, .contacts-card, .quote blockquote'
);

if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  revealTargets.forEach(el => {
    el.classList.add('reveal');
    io.observe(el);
  });
} else {
  revealTargets.forEach(el => el.classList.add('in'));
}

// --- лёгкая тень шапки при прокрутке ---
const header = document.querySelector('.site-header');
if (header) {
  const onScroll = () => {
    header.classList.toggle('is-scrolled', window.scrollY > 12);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}
