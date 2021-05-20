#!/bin/bash
aws ecr get-login-password --region eu-west-1 > ecr-pwd.txt
ecr_pwd=`cat ecr-pwd.txt`
rm ecr-pwd.txt
docker login -u AWS -p $ecr_pwd 853628181016.dkr.ecr.eu-west-1.amazonaws.com
docker tag ml-boilerplate/client 853628181016.dkr.ecr.eu-west-1.amazonaws.com/ml-boilerplate/client
docker push 853628181016.dkr.ecr.eu-west-1.amazonaws.com/ml-boilerplate/client
docker tag ml-boilerplate/api 853628181016.dkr.ecr.eu-west-1.amazonaws.com/ml-boilerplate/api
docker push 853628181016.dkr.ecr.eu-west-1.amazonaws.com/ml-boilerplate/api