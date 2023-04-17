# 動漫列表 / Anime List

Record your own anime watch list, focusing on simplicity. No too much fancy features.

This project is a rewrite version of my personal version, originally written in php. That is how I learn php and html, so you can imagine how messy is it. You can still see the messy frontend code with all javascript functions squeezed in a single `main.js` file.

## Try it out

If you want to try this app, great. You can host it yourself.

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