set MANAGE=.pve\scripts\python src\manage.py

%MANAGE% assets build
%MANAGE% collectstatic --noinput
git add styles static assets templates
git commit -m deploy
git push production
