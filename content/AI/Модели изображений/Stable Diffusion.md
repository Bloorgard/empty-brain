## О моделях

Stable Diffusion — семейство генеративных моделей изображений; условия использования зависят от версии и лицензии. Помимо базовых моделей (обученных в Stability AI) существует огромная экосистема дообученных версий. Базовую модель можно дообучать на своих данных, получая специализированные результаты. Результат дообучения — либо файл, заменяющий основную модель, либо подключаемый дополнительно.

Актуальная отправная точка — [карточка Stable Diffusion 3.5 Large](https://huggingface.co/stabilityai/stable-diffusion-3.5-large)
с условиями доступа и лицензией. Это пример более нового поколения, а не утверждение,
что все инструменты и дообучения ниже совместимы с ним.

Типы моделей:
- Чекпоинты — заменяют основной файл модели
- Лоры — подключаются дополнительно к чекпоинту
- Текстовая инверсия (эмбеддинги)

### Каталоги

- [Civitai](https://civitai.com/)
- [Huggingface diffusers gallery](https://huggingface.co/spaces/huggingface-projects/diffusers-gallery)
- [Ветка Reddit r/StableDiffusion](https://www.reddit.com/r/StableDiffusion)

## Запуск

[[Модели изображений]]

## Чекпоинты SD 1.5

Архивная подборка для старых workflow. Не переносится автоматически на SDXL,
SD 3.x или FLUX. У каждого дообучения нужно проверять базовую модель.

На 29 октября 2026 года карточки Reliberate, Deliberate, LowRA, Lit и Acid Mix
из прежнего списка не найдены: страницы и API Civitai возвращают 404.
Их адреса сохранены в отчёте ревью; модель на другом сайте или под другим ID не проверялась.

### Универсальные
- [CyberRealistic](https://civitai.com/models/15003/cyberrealistic?modelVersionId=114429)

#### Паттерны
- [Floral patterns](https://civitai.com/models/26295/floral-patterns)
- [Floral patterns merge](https://civitai.com/models/26464/floral-patterns-merge)

#### Арты
- [DGSpitzer Art Diffusion](https://civitai.com/models/4787/dgspitzer-art-diffusion)
- [Город грехов](https://civitai.com/models/1228/sin-city-movie-style)

#### Лоры
- [Chrome tech](https://civitai.com/models/118153/chrome-tech-world-morph)

### Абстрактные
- [hylv6](https://civitai.com/models/115188/hylv6) — капельки пурпура
- [Holographic model](https://civitai.com/models/28778/holographic-model)

### Иллюстративные
- [graphic-art](https://civitai.com/models/7884/graphic-art)
- [illustration model](https://civitai.com/models/25898/illustration-model)
- [Game Icon Institute](https://civitai.com/models/47800/game-icon-institutemode)
- [T-shirt print designs](https://civitai.com/models/5256/t-shirt-print-designs-test-model)

#### Для QR
- [Fantasy World](https://civitai.com/models/107151/fantasy-world)
- [Stoked Illustration](https://civitai.com/models/81959/stoked-illustration)
- [comi-noir-v2](https://civitai.com/models/16325/comi-noir-v2)

### Стилёвое
- [SynthwavePunk](https://civitai.com/models/1102/synthwavepunk)
- [JIM EIDOMODE](https://civitai.com/models/10720/jim-eidomode)
- [Pareidolia Gateway](https://civitai.com/models/1242/pareidolia-gateway)

### Дизайнерские

#### Объекты
- [MotionDesignV1](https://civitai.com/models/92770/motiondesignv1-3dartc4d-style)
- [Arthemy Objects](https://civitai.com/models/88128/arthemy-objects)
- [Product Design (minimalism-eddiemauro)](https://civitai.com/models/23893/product-design-minimalism-eddiemauro)

#### 3D
- [Bdicon](https://civitai.com/models/100056/bdicon) — 3D иконки
- [businessdesign](https://civitai.com/models/116495/businessdesign)
- [Плюш](https://civitai.com/models/9668/plushies)

### Нужно затестить
- [pseudo-flex-base](https://civitai.com/models/97808/pseudo-flex-base)
- [ColorfulSurrealismAI](https://civitai.com/models/12437/colorfulsurrealismai)
- [2.8D STABLE BEST VERSION](https://civitai.com/models/77446/28d-stable-best-version)
- [StretchScape](https://civitai.com/models/99310/stretchscape) — широкие пейзажи
- [Pirsus Artstation](https://civitai.com/models/97669/pirsus-artstation)
- [AC pencil](https://civitai.com/models/20631/ac-pencil)
- [SDVN3-RealArt](https://civitai.com/models/103160?modelVersionId=117136)
- [Abstract Photo](https://civitai.com/models/95973/abstract-photo)
- [China-Chic-illustration](https://huggingface.co/tilake/China-Chic-illustration)

## Чекпоинты SD 2.x

- [DesignMeld](https://civitai.com/models/23263?modelVersionId=27783) — в карточке указана база Stable Diffusion 2.x; перенесён из ошибочной группы SD 1.5

## ControlNet

- [QR-codes SD 1.5](https://huggingface.co/monster-labs/control_v1p_sd15_qrcode_monster/resolve/main/control_v1p_sd15_qrcode_monster.safetensors)
- [ControlNet SDXL 1.0](https://replicate.com/lucataco/sdxl-controlnet)

## Статьи
- [Текстовая инверсия на пяти картинках](https://www.reddit.com/r/StableDiffusion/comments/wvzr7s/tutorial_fine_tuning_stable_diffusion_using_only/)
- [Как вписать человека в любое фото с помощью SD и Automatic1111](https://dtf.ru/howto/1751351-kak-vpisat-cheloveka-v-lyuboe-foto-s-pomoshchyu-stable-diffusion-i-automatic1111)
- [Написание промптов для SD: подборка инструментов и оптимизация](https://dtf.ru/u/801655-phygital/1871114-napisanie-promptov-dlya-stable-diffusion-podborka-instrumentov-i-optimizaciya)

## Видосы
- [Похожие лица с помощью CN](https://www.youtube.com/watch?v=tBwmbTwMxfQ&ab_channel=SebastianKamph)
- [Изменение света в генерации](https://www.youtube.com/watch?v=_xHC3bT5GBU&t=291s&ab_channel=SebastianKamph)
- [Аутпеинт](https://www.youtube.com/watch?v=bRViS8MEElI&ab_channel=StableDiff)

## Промпты
- [SD V1 Modifier Studies](https://proximacentaurib.notion.site/2b07d3195d5948c6a7e5836f9d535592?v=b5b75a67cc52483c9965cfc141f6f582)
- [Генератор промптов](https://promptomania.com/creative-fabrica-spark-prompt-builder/)
