#!/bin/bash
APP_NAME=laerdal-ml-boilerplate-api
heroku container:login
heroku create $APP_NAME
docker tag ml-boilerplate/api registry.heroku.com/$APP_NAME/web
docker push registry.heroku.com/$APP_NAME/web
heroku container:release --app $APP_NAME web
heroku ps:scale --app $APP_NAME web=1
heroku ps --app $APP_NAME
heroku logs --app $APP_NAME --tail