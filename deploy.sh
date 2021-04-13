#! /bin/bash
heroku container:login
heroku container:push --recursive -a github-ify
heroku container:release web clock -a github-ify
heroku ps:scale clock=1 -a github-ify