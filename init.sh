#!/bin/bash
flask db upgrade
exec gunicorn -b :8000 -w 4 'finance_app:create_app()'