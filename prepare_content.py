"""Prepare locally verified Yandex Maps content and web-sized photographs."""
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'

def read(name):
    return json.loads((DATA / name).read_text(encoding='utf-8'))

def write(name, data):
    (DATA / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def price(p):
    return p.get('price') or int(re.sub(r'\D', '', p['priceText']))

source = read('yandex-products.json')
products = source['products']
selected = [
    (0, '15 роз', 'Россия · 50 см · авторское оформление', 'roses'),
    (1, '25 роз', 'Россия · 50 см · авторское оформление', 'roses'),
    (2, 'Французские розы в коробке', '11 роз · металлическая шляпная коробка', 'boxes'),
    (3, '35 роз под ленту', 'Россия · 60 см', 'roses'),
    (4, '23 розы с тишью', 'Россия · 50 см · авторское оформление', 'roses'),
    (5, '51 роза', 'Россия · 50 см · авторское оформление', 'roses'),
    (6, '101 роза', 'Россия · 50 см · авторское оформление', 'roses'),
    (7, 'Нежный микс из 51 розы', 'Россия · 60 см · авторское оформление', 'roses'),
    (8, 'Нежный микс из 45 роз', 'Эквадор · в оформлении', 'roses'),
    (9, '51 роза под ленту', 'Россия · 60 см', 'roses'),
    (10, '101 роза, 60 см', 'Россия · авторское оформление', 'roses'),
    (11, '51 роза в корзине', 'Россия · 50 см', 'baskets'),
    (18, 'Диантусы и эвкалипт', '19 диантусов · 8 веток эвкалипта', 'mixed'),
    (19, 'Сборный с хризантемами', 'Диантусы · эвкалипт · хризантемы', 'mixed'),
    (20, 'Диантусы и альстромерии', '15 диантусов · 6 альстромерий', 'mixed'),
    (21, 'Диантусы в коробке', '15 диантусов · 7 веток эвкалипта', 'boxes'),
    (22, 'Гипсофила в коробке', '7 белых гипсофил · шляпная коробка', 'boxes'),
    (23, 'Розы и эвкалипт', '13 роз Эквадор · 5 веток эвкалипта', 'mixed'),
    (30, 'Сборный в коробке', 'Диантусы · кустовые диантусы · эвкалипт', 'boxes'),
    (31, 'Розы с кустовыми розами', '7 роз Россия · 4 кустовые розы · эвкалипт', 'mixed'),
    (32, '11 роз и эвкалипт', 'Розы Эквадор · авторское оформление', 'mixed'),
    (33, '17 роз и эвкалипт', 'Россия · 50 см · авторское оформление', 'mixed'),
    (34, '51 роза с эвкалиптом', 'Россия · 60 см · оформление с тишью', 'mixed'),
    (36, '15 роз и эвкалипт', 'Россия · 60 см · авторское оформление', 'mixed'),
]

catalog = []
for index, title, description, category in selected:
    p = products[index]
    if not p.get('image'):
        raise ValueError(f'Missing verified image: {index}')
    catalog.append(dict(id=f'bouquet-{index:03d}', sourceIndex=index, sourceName=p['name'], name=title,
                        description=description, category=category, price=price(p),
                        sourceImage=p['image'], image=f'assets/catalog/bouquet-{index:03d}.jpg'))

gift_names = ['Зайка Роза ( 20-25см )', 'Зайка София 50 см', 'Радужный Тедди 50см',
              'Плюшевый Коржик 50см', 'Авокадо 65см', 'Мишка Оливер', 'Медведь Степа 50см', 'Мишка Стёпа (40 см)']
for n, name in enumerate(gift_names):
    p = next(p for p in products if p['name'] == name)
    if not p.get('image'):
        raise ValueError(f'Missing verified gift image: {name}')
    catalog.append(dict(id=f'gift-{n:02d}', sourceIndex=p['index'], sourceName=p['name'], name=p['name'],
                        description='50 см' if p['name']=='Мишка Оливер' else ('Цвет платья зависит от наличия' if 'София' in p['name'] else 'Мягкая игрушка к вашему букету'),
                        category='gifts', price=price(p),
                        sourceImage=p['image'], image=f'assets/catalog/gift-{n:02d}.jpg'))

gallery = read('yandex-gallery.json')
for i, photo in enumerate(gallery['photos']):
    photo['image'] = f'assets/gallery/shop-{i+1:02d}.jpg'

jobs = [(p['sourceImage'].rsplit('/',1)[0]+'/orig', p['image']) for p in catalog]
jobs += [(p['src'], p['image']) for p in gallery['photos']]

def download(job):
    url, relative = job
    destination = ROOT / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with urlopen(request, timeout=45) as response:
        raw = response.read()
    with Image.open(BytesIO(raw)) as original:
        img = ImageOps.exif_transpose(original).convert('RGB')
        img.thumbnail((900, 1100))
        img.save(destination, 'JPEG', quality=85, optimize=True, progressive=True)
        return relative, img.size

with ThreadPoolExecutor(max_workers=6) as pool:
    sizes = dict(pool.map(download, jobs))
for p in catalog:
    p['width'], p['height'] = sizes[p['image']]
for p in gallery['photos']:
    p['width'], p['height'] = sizes[p['image']]
write('catalog.json', dict(source=source['source'], checked=source['checked'], products=catalog))
write('yandex-gallery.json', gallery)

# Keep facts and source locations, rather than reproducing promotional paragraphs.
for p in products:
    description = p.pop('description', p.get('composition', ''))
    composition = description.split('В нашем магазине')[0].strip()
    if composition.startswith(('Состав', '7 роз')):
        p['composition'] = composition
    p['price'] = price(p)
    p.pop('priceText', None)
write('yandex-products.json', source)

reviews_source = read('yandex-reviews.json')
summaries = [
    'Букеты по образцу, аккуратное оформление и внимательные флористы. Подарки на дни рождения понравились получателям.',
    'Повторные заказы, свежие цветы и помощь с выбором. Покупательница отмечает доставку и связь во время подготовки.',
    'Красные розы в подарок: покупательница осталась довольна цветами и доставкой к согласованному времени.',
    'Магазин выручил со срочным букетом. Покупательница отмечает выбор роз, быструю сборку и подкормку для цветов.',
    'Покупательница возвращается за цветами и отмечает аккуратную упаковку, свежесть и своевременную доставку.',
    'Покупательница хвалит стойкость букетов и быстрые ответы на сообщения. Заказывает здесь повторно.',
]
review_records = []
for i, r in enumerate(reviews_source['reviews']):
    record = {key: value for key,value in r.items() if key!='text'}
    if i < len(summaries):
        record['summary'] = summaries[i]
        review_records.append(record)
reviews_source['reviews'] = review_records
reviews_source['presentation'] = 'Selected reviews, paraphrased; not verbatim quotations.'
write('yandex-reviews.json', reviews_source)

def contact_sheet(paths, filename, columns=6):
    cell_w, cell_h = 170, 240
    canvas = Image.new('RGB',(columns*cell_w, ((len(paths)+columns-1)//columns)*cell_h),'white')
    draw = ImageDraw.Draw(canvas)
    for i, relative in enumerate(paths):
        with Image.open(ROOT/relative) as img:
            thumb = ImageOps.contain(img,(cell_w-8,cell_h-28))
            x,y = (i%columns)*cell_w, (i//columns)*cell_h
            canvas.paste(thumb,(x+(cell_w-thumb.width)//2,y))
            draw.text((x+5,y+cell_h-23), Path(relative).stem, fill='black')
    canvas.save(DATA/filename)
contact_sheet([p['image'] for p in catalog], 'catalog-contact-sheet.jpg')
contact_sheet([p['image'] for p in gallery['photos']], 'gallery-contact-sheet.jpg',4)
print(json.dumps({'catalogProducts':len(catalog),'galleryPhotos':len(gallery['photos']),'imageBytes':sum((ROOT/p).stat().st_size for _,p in jobs)},ensure_ascii=False))
