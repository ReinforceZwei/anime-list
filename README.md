# 動漫列表 / Anime List

<img align="right" height="128px" width="128px" src="animeList/static/css/data/Anime-round-min.png">

Record your own anime watch list, focusing on simplicity. No too much fancy features.

This project is a rewrite version of my personal version, originally written in php. That is how I learn php and html, so you can imagine how messy is it. You can still see the messy frontend code with all javascript functions squeezed in a single `main.js` file.

## Try it out

If you want to try this app, great. A demo instance is available at [anime.saku.moe](https://anime.saku.moe/). Login with `demo/demo` or create a new account.

Or you can host it yourself.

### Docker compose

Pull pre-build image from `ghcr.io/reinforcezwei/anime-list:latest`

`amd64`, `arm64` and `armv7` are available.

```yml
version: "3.9"
services:
  app:
    image: ghcr.io/reinforcezwei/anime-list:latest
    environment:
      PORT: 5000
      DB_HOST: db
      DB_USER: "root"
      DB_PASSWORD: "ChangeMe!"
      SECRET_KEY: "ChangeMeToo!"
    ports:
      - "5000:5000"
    depends_on:
      - db
    restart: on-failure
  db:
    image: mariadb
    restart: always
    environment:
      MARIADB_ROOT_PASSWORD: ChangeMe!
```

### Manual install

- First you will need a MySQL/MariaDB server
- Python version 3.10 or above (IMPORTANT!)
- Download project source code
- Make a copy of `.env.example` file and name it `.env`
- Change your settings in `.env` file
  - Your database user must have permissions to create databases and tables
  - Remember to change secret key or just make it empty. One-time secret will be generated
- You can also set environment variables directly
- Install requirements `pip install -r requirements.txt`
- Launch a test instance `python animeList/app.py`
- Go to `http://localhost:<your_port>`

If you would like to host a production instance, remember to use a production WSGI server as warned by flask, and put it behind a HTTPS reverse proxy like nginx or caddy. If resources are available, you can also deploy a WAF (Web Application Firewall)