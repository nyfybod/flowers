"""Render sourced content into the existing Rose 73 landing page."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parent
def read(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))
def money(price):
    return f'{price:,}'.replace(',', '\u202f') + ' ₽'

catalog = read('catalog.json')
reviews = read('yandex-reviews.json')
gallery = read('yandex-gallery.json')
source = catalog['source']

def photo_button(p, extra_class=''):
    return f'''<button type="button" class="content-photo {extra_class}" data-photo="{escape(p['image'])}" data-caption="{escape(p['name'])}" data-photo-price="{p.get('price', '')}" aria-label="Рассмотреть: {escape(p['name'])}"><img src="{escape(p['image'])}" alt="{escape(p.get('sourceName',p['name']))}" width="{p['width']}" height="{p['height']}" loading="lazy" decoding="async"><span class="photo-expand" aria-hidden="true">↗</span></button>'''

def product_card(p):
    kind = 'gift-card' if p['category']=='gifts' else 'catalog-card'
    return f'''<article class="{kind}" data-category="{p['category']}" data-price="{p['price']}" id="{p['id']}">
      {photo_button(p)}
      <div class="product-info"><h3>{escape(p['name'])}</h3><p>{escape(p['description'])}</p><div class="product-bottom"><strong class="product-price">{money(p['price'])}</strong><a class="product-order" href="tel:+79053491188" aria-label="Уточнить заказ: {escape(p['name'])}">Заказать <span aria-hidden="true">↗</span></a></div></div>
    </article>'''

order = [0,22,1,20,2,18,11,3,21,23,5,30,4,6,7,8,9,10,19,31,32,33,34,36]
flower_products = sorted([p for p in catalog['products'] if p['category']!='gifts'], key=lambda p:order.index(p['sourceIndex']))
gift_products = [p for p in catalog['products'] if p['category']=='gifts']

catalog_section = f'''<!-- BEGIN SOURCED CATALOG -->
    <section class="shop-catalog section-pad" id="catalog" aria-labelledby="catalog-title">
      <div class="section-head"><div><p class="section-kicker">Букеты с ценами</p><h2 id="catalog-title">Выберите свой<br><em>букет</em></h2></div><p class="section-note">Розы, сборные букеты и композиции.<br>Фотографии и цены — из карточки Rose 73.</p></div>
      <div class="catalog-toolbar"><div class="catalog-filters" role="group" aria-label="Вид букета"><button type="button" data-catalog-filter="all" aria-pressed="true">Все букеты</button><button type="button" data-catalog-filter="roses" aria-pressed="false">Розы</button><button type="button" data-catalog-filter="mixed" aria-pressed="false">Сборные</button><button type="button" data-catalog-filter="boxes" aria-pressed="false">В коробке</button><button type="button" data-catalog-filter="baskets" aria-pressed="false">В корзине</button></div><label class="budget-toggle"><input type="checkbox" id="budget-filter"> До 3 000 ₽</label></div>
      <div class="catalog-grid">{''.join(product_card(p) for p in flower_products)}</div>
      <div class="catalog-empty" hidden><h3>В этой подборке нет букетов до 3 000 ₽</h3><p>Снимите ограничение по цене или обсудите свой бюджет с флористом.</p><button type="button" class="button button-solid" id="reset-catalog">Сбросить фильтры</button></div>
      <div class="catalog-pagination"><p id="catalog-status" role="status">24 букета с фотографиями и ценами</p><button type="button" class="button catalog-more" id="catalog-more" hidden>Показать ещё 6 букетов <span aria-hidden="true">↓</span></button></div>
      <p class="source-note">Цены проверены 9 ноября 2026 года по <a href="{source}" target="_blank" rel="noopener noreferrer">прайсу на Яндекс Картах ↗</a>. В источнике: «Обновлено 21 августа». Состав, оттенки, упаковка и наличие могут отличаться — подтвердите итоговую стоимость перед заказом.</p>
    </section>
    <!-- END SOURCED CATALOG -->'''

gift_section = f'''<!-- BEGIN SOURCED GIFTS -->
    <section class="shop-gifts section-pad" id="gifts" aria-labelledby="gifts-title"><div class="section-head"><div><p class="section-kicker">Дополните подарок</p><h2 id="gifts-title">Больше<br><em>тёплых объятий</em></h2></div><p class="section-note">Мягкие игрушки из ассортимента Rose 73.<br>Цветы на фото с игрушками оплачиваются отдельно.</p></div><div class="gifts-grid">{''.join(product_card(p) for p in gift_products)}</div><p class="source-note">Указана цена одной игрушки. Наличие и расцветку уточняйте у флориста. Источник и дата проверки цен — те же, что в каталоге букетов.</p></section>
    <!-- END SOURCED GIFTS -->'''

services_section = '''<!-- BEGIN SOURCED SERVICES -->
    <section class="shop-services section-pad" id="services" aria-labelledby="services-title"><div class="section-head"><div><p class="section-kicker">Не только букеты</p><h2 id="services-title">Поможем сделать<br><em>приятно</em></h2></div><p class="section-note">Услуги и возможности, указанные<br>в карточке магазина.</p></div><div class="services-grid">
    <article><span class="service-symbol" aria-hidden="true">↗</span><h3>Доставка цветов</h3><p>Цветы и букеты по Ульяновску. Адрес, удобное время и стоимость согласуем при заказе.</p><span class="service-price">Стоимость — по согласованию</span></article>
    <article><span class="service-symbol" aria-hidden="true">♡</span><h3>Свадебная флористика</h3><p>Букет невесты и цветочные композиции. Расскажите о дате, оттенках и ваших пожеланиях.</p><span class="service-price">Стоимость — по согласованию</span></article>
    <article><span class="service-symbol" aria-hidden="true">✿</span><h3>Упаковка подарков</h3><p>Подарочная упаковка, поздравительные открытки и мягкие игрушки к вашему букету.</p><span class="service-price">Упаковка — по согласованию</span></article>
    <article><span class="service-symbol" aria-hidden="true">⌂</span><h3>Самовывоз</h3><p>Заберите заказ в магазине: Ульяновск, 2-й пер. Мира, 31. Время готовности уточните у флориста.</p><a href="tel:+79053491188" class="service-phone">Согласовать заказ ↗</a></article>
    </div><p class="source-note">Отдельный тариф на доставку, упаковку и свадебную флористику в источнике не опубликован. <a href="https://yandex.com/maps/org/rose_73/88956342072/?tab=features" target="_blank" rel="noopener noreferrer">Особенности магазина на Яндекс Картах ↗</a></p></section>
    <!-- END SOURCED SERVICES -->'''

gallery_alts = ['Вход в цветочный магазин Rose 73 на 2-м переулке Мира', 'Букет ярких роз из галереи Rose 73', 'Витрина магазина Rose 73', 'Розово-малиновые тюльпаны в упаковке', 'Большой розовый букет из галереи Rose 73', 'Цветы и готовые букеты на витрине', 'Розовые хризантемы в магазине Rose 73']
gallery_items = []
for i in [0,1,3,4,5,6]:
    p = gallery['photos'][i]
    p['name'] = gallery_alts[i]
    p['alt'] = gallery_alts[i]
    gallery_items.append(photo_button(p, 'gallery-photo'))
gallery_section = f'''<!-- BEGIN SOURCED GALLERY -->
    <section class="shop-gallery section-pad" id="gallery" aria-labelledby="gallery-title"><div class="section-head"><div><p class="section-kicker">Фотографии магазина</p><h2 id="gallery-title">Наши цветы.<br><em>Ваши поводы.</em></h2></div><a class="link-underline" href="{gallery['source']}" target="_blank" rel="noopener noreferrer">Больше фото на Яндекс Картах ↗</a></div><div class="gallery-grid">{''.join(gallery_items)}</div><p class="source-note">Фотографии из карточки Rose 73. Нажмите на снимок, чтобы рассмотреть его крупнее. Букеты в галерее — примеры работ, их стоимость уточняется отдельно.</p></section>
    <!-- END SOURCED GALLERY -->'''

review_cards = []
for r in reviews['reviews']:
    date = r['date'][:10]
    year = date[:4]
    label = r['dateLabel'] if year in r['dateLabel'] else r['dateLabel']+' '+year
    initials = ''.join(part[0] for part in r['author'].split()[:2])
    review_cards.append(f'''<article class="review-card"><div class="review-head"><span class="review-avatar" aria-hidden="true">{escape(initials)}</span><div><a href="{escape(r['authorUrl'])}" target="_blank" rel="noopener noreferrer">{escape(r['author'])}</a><time datetime="{date}">{escape(label)}</time></div></div><span class="review-stars" aria-label="5 из 5">★★★★★</span><p>{escape(r['summary'])}</p><a class="review-source" href="{reviews['source']}" target="_blank" rel="noopener noreferrer">Оригинал на Яндекс Картах ↗</a></article>''')
reviews_section = f'''<!-- BEGIN SOURCED REVIEWS -->
    <section class="shop-reviews section-pad" id="reviews" aria-labelledby="reviews-title"><div class="section-head"><div><p class="section-kicker">Истории покупателей</p><h2 id="reviews-title">Спасибо<br><em>за ваше доверие</em></h2></div><a class="review-rating" href="{reviews['source']}" target="_blank" rel="noopener noreferrer"><strong>5,0 <span aria-hidden="true">★</span></strong><span>277 оценок · 202 отзыва<br>на Яндекс Картах ↗</span></a></div><div class="reviews-grid">{''.join(review_cards)}</div><p class="source-note">Выбранные отзывы с Яндекс Карт: краткое содержание, не дословные цитаты. Имена, даты и оценки сохранены. Рейтинг и количество отзывов проверены 9 ноября 2026 года. <a href="{reviews['source']}" target="_blank" rel="noopener noreferrer">Читать все отзывы ↗</a></p></section>
    <!-- END SOURCED REVIEWS -->'''

viewer = '''<!-- BEGIN PHOTO VIEWER -->
  <dialog id="photo-viewer" class="photo-viewer" aria-labelledby="photo-caption"><button type="button" class="photo-viewer-close" aria-label="Закрыть фотографию">×</button><figure><img id="viewer-image" alt=""><figcaption><h2 id="photo-caption"></h2><p id="photo-price"></p></figcaption></figure><div class="viewer-actions"><button type="button" id="photo-prev" aria-label="Предыдущая фотография">←</button><p id="photo-position" role="status"></p><button type="button" id="photo-next" aria-label="Следующая фотография">→</button></div></dialog>
  <!-- END PHOTO VIEWER -->'''

path = ROOT / 'index.html'
html = path.read_text(encoding='utf-8')
for name in ['CATALOG','GIFTS','SERVICES','GALLERY','REVIEWS']:
    html = re.sub(r'\s*<!-- BEGIN SOURCED '+name+r' -->.*?<!-- END SOURCED '+name+r' -->', '', html, flags=re.S)
html = re.sub(r'\s*<!-- BEGIN PHOTO VIEWER -->.*?<!-- END PHOTO VIEWER -->', '', html, flags=re.S)
html = html.replace('    <!-- ============ BOUQUETS ============ -->', catalog_section+'\n\n    <!-- ============ BOUQUETS ============ -->')
html = html.replace('    <!-- ============ ABOUT ============ -->', gift_section+'\n\n'+services_section+'\n\n    <!-- ============ ABOUT ============ -->')
html = html.replace('    <!-- ============ CONTACTS ============ -->', gallery_section+'\n\n'+reviews_section+'\n\n    <!-- ============ CONTACTS ============ -->')
html = html.replace('  <script src="script.js"></script>', viewer+'\n\n  <script src="script.js"></script>')
html = html.replace('<a href="#bouquets">Букеты</a>', '<a href="#catalog">Букеты и цены</a>')
if '<a href="#services">Услуги</a>' not in html:
    html = html.replace('<a href="#about">О магазине</a>', '<a href="#about">О магазине</a>\n      <a href="#services">Услуги</a>\n      <a href="#reviews">Отзывы</a>')
html = html.replace('href="#bouquets">Смотреть букеты', 'href="#catalog">Смотреть букеты')
html = html.replace('Цены и наличие зависят от сезона и поставки —<br />\n          уточните по телефону, и мы подскажем варианты.', 'Не нашли подходящий букет в каталоге?<br />\n          Подберём цветы под ваш повод и бюджет.')
html = html.replace('Звонок или сообщение — как удобнее', 'Оплата наличными, картой или по QR-коду')
path.write_text(html, encoding='utf-8')
print('Rendered 24 bouquets, 8 gifts, 6 gallery photos, 6 review summaries and 4 service cards.')
