#!/bin/bash
heroku container:login
heroku create laerdal-ml-boilerplate
docker tag ml-boilerplate/api registry.heroku.com/laerdal-ml-boilerplate/web
docker push registry.heroku.com/laerdal-ml-boilerplate/web
heroku container:release web
heroku open
