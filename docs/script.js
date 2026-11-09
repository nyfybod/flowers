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

// Каталог: фильтр по виду и бюджету, порционная выдача.
(() => {
  const catalog = document.querySelector('.catalog-grid');
  if (!catalog) return;
  const cards = Array.from(catalog.querySelectorAll('.catalog-card'));
  const filters = Array.from(document.querySelectorAll('[data-catalog-filter]'));
  const budget = document.querySelector('#budget-filter');
  const more = document.querySelector('#catalog-more');
  const status = document.querySelector('#catalog-status');
  const empty = document.querySelector('.catalog-empty');
  const reset = document.querySelector('#reset-catalog');
  let category = 'all';
  let limit = 6;

  function updateCatalog() {
    const matches = cards.filter(card =>
      (category === 'all' || card.dataset.category === category) &&
      (!budget.checked || Number(card.dataset.price) <= 3000)
    );
    cards.forEach(card => { card.hidden = true; });
    matches.slice(0, limit).forEach(card => { card.hidden = false; });
    const remaining = matches.length - limit;
    more.hidden = remaining <= 0;
    more.textContent = `Показать ещё ${Math.min(6, Math.max(0, remaining))} ↓`;
    status.textContent = matches.length
      ? `Показано ${Math.min(limit, matches.length)} из ${matches.length}`
      : 'По выбранным условиям букеты не найдены';
    empty.hidden = matches.length > 0;
  }
  filters.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.catalogFilter;
    limit = 6;
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    updateCatalog();
  }));
  budget.addEventListener('change', () => { limit = 6; updateCatalog(); });
  more.addEventListener('click', () => {
    const visibleBefore = new Set(cards.filter(card => !card.hidden));
    limit += 6;
    updateCatalog();
    // Переводим фокус на первый добавленный товар, сохраняя порядок чтения.
    cards.find(card => !card.hidden && !visibleBefore.has(card))
      ?.querySelector('button')?.focus({ preventScroll: true });
  });
  reset.addEventListener('click', () => {
    category = 'all';
    budget.checked = false;
    limit = 6;
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.catalogFilter === 'all')));
    updateCatalog();
    filters[0].focus();
  });
  updateCatalog();
})();

// Оригинальные фотографии: модальное окно с управлением с клавиатуры.
(() => {
  const viewer = document.querySelector('#photo-viewer');
  if (!viewer) return;
  const image = document.querySelector('#viewer-image');
  const caption = document.querySelector('#photo-caption');
  const price = document.querySelector('#photo-price');
  const position = document.querySelector('#photo-position');
  const photoButtons = Array.from(document.querySelectorAll('[data-photo]'));
  const currency = new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 });
  let photos = [];
  let index = 0;
  let trigger = null;

  function showPhoto() {
    const photo = photos[index];
    image.src = photo.dataset.photo;
    image.alt = photo.dataset.caption;
    caption.textContent = photo.dataset.caption;
    price.textContent = photo.dataset.photoPrice
      ? `${currency.format(Number(photo.dataset.photoPrice))} · Цена по карточке на Яндекс Картах, проверена 09.11.2026. Наличие уточняйте.`
      : 'Фото из галереи Rose 73 на Яндекс Картах. Стоимость букета уточняйте отдельно.';
    position.textContent = `${index + 1} из ${photos.length}`;
  }
  function move(direction) {
    index = (index + direction + photos.length) % photos.length;
    showPhoto();
  }
  photoButtons.forEach(button => button.addEventListener('click', () => {
    trigger = button;
    const group = button.closest('.catalog-grid, .gifts-grid, .gallery-grid');
    photos = Array.from(group.querySelectorAll('[data-photo]'))
      .filter(photo => !photo.closest('[hidden]'));
    index = photos.indexOf(button);
    showPhoto();
    viewer.showModal();
  }));
  document.querySelector('.photo-viewer-close').addEventListener('click', () => viewer.close());
  document.querySelector('#photo-prev').addEventListener('click', () => move(-1));
  document.querySelector('#photo-next').addEventListener('click', () => move(1));
  viewer.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      move(event.key === 'ArrowLeft' ? -1 : 1);
    }
  });
  viewer.addEventListener('click', event => {
    if (event.target !== viewer) return;
    const bounds = viewer.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) viewer.close();
  });
  viewer.addEventListener('close', () => trigger?.focus({ preventScroll: true }));
})();
