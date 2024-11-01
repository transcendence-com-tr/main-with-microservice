@echo off
title transcendence

start cmd /k "title Server 8000 & python services/auth/manage.py runserver 0.0.0.0:8000"
start cmd /k "title Server 80 & python frontend/manage.py runserver 0.0.0.0:80"

pause
