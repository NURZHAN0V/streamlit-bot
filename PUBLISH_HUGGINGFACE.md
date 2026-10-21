# Публикация чат-бота на Hugging Face

## Как сделать примерно за 10 минут

Расчёт на то, что аккаунт Hugging Face уже создан, а `main.py` и `requirements.txt` готовы. Первая сборка может занять ещё несколько минут.

### 1. Создайте Space

1. Зарегистрируйтесь на [huggingface.co](https://huggingface.co/) и войдите в аккаунт.
2. Нажмите **New Space**.
3. Придумайте имя для сайта.
4. В списке **SDK** выберите **Docker**. Отдельного варианта Streamlit сейчас нет, поэтому приложение Streamlit запускается внутри Docker Space.
5. Выберите видимость. При варианте **Public** любой сможет открыть сайт и увидеть файлы программы. Не записывайте секретный ключ в файлы программы.
6. Перед созданием проверьте условия и цену выбранного Docker Space: доступность бесплатного варианта зависит от текущих условий Hugging Face.

### 2. Добавьте файлы приложения

Загрузите `main.py` и `requirements.txt`. Если файла `requirements.txt` ещё нет, создайте его и запишите:

```text
streamlit
requests
```

Также создайте в Space два небольших файла: `README.md` и `Dockerfile`.

В `README.md` вставьте:

```yaml
---
title: Учебный чат-бот
sdk: docker
app_port: 7860
---
```

В `Dockerfile` вставьте:

```dockerfile
FROM python:3.11-slim

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
WORKDIR /home/user/app

COPY --chown=user requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt
COPY --chown=user main.py ./

EXPOSE 7860
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=7860"]
```

Этот файл объясняет Hugging Face, как установить нужные библиотеки и запустить сайт.

### 3. Добавьте ключ Timeweb

Ключ берётся в кабинете Timeweb, а не на Hugging Face.

1. Откройте страницу Space и перейдите в **Settings**.
2. Найдите раздел **Variables and secrets** и добавьте **Secret**.
3. В поле имени укажите `TIMEWEB_API_KEY`, а в поле значения вставьте API-ключ Timeweb.
4. Сохраните секрет. Не добавляйте ключ в `main.py`, `README.md` или другие загружаемые файлы.

В `main.py` строка чтения ключа должна поддерживать локальную настройку и Hugging Face:

```python
API_KEY = os.getenv("TIMEWEB_API_KEY") or st.secrets["TIMEWEB_API_KEY"]
```

Для этой строки в начале `main.py` также нужен `import os`. На Hugging Face ключ будет передан программе автоматически из настроек Space. На компьютере он возьмётся из `.streamlit/secrets.toml`.

Для обычного обращения к API Timeweb по HTTPS не нужно открывать входящие порты или разрешать подключения с любых IP в firewall.

### 4. Запустите сайт

Откройте вкладку Space и дождитесь окончания сборки. Если появится ошибка, откройте **Logs** и проверьте сообщения. После успешного запуска Hugging Face покажет ссылку примерно такого вида:

```text
https://имя-пользователя-имя-space.hf.space
```

Точную ссылку берите со страницы Space. Сайт находится в облаке, поэтому ваш компьютер не должен оставаться включённым. На бесплатном тарифе приложение может засыпать, когда им долго не пользуются.
