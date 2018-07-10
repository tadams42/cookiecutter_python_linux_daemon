#!/bin/sh

git init .
git commit --allow-empty -m "Initial"
git checkout -b development

cd config
ln -s ../src/{{cookiecutter.project_slug}}/resources/development.yaml
ln -s ../src/{{cookiecutter.project_slug}}/resources/test.yaml
ln -s ../src/{{cookiecutter.project_slug}}/resources/logging_config.json
cd ..

git add .
git commit -m "Application scaffold"

