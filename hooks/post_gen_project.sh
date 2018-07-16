#!/bin/sh

if [ ! -d ".git" ]; then
    git init .
    git commit --allow-empty -m "Initial"
    git checkout -b development

    cd config
    ln -sf ../src/{{cookiecutter.project_slug}}/resources/development.yaml
    ln -sf ../src/{{cookiecutter.project_slug}}/resources/test.yaml
    ln -sf ../src/{{cookiecutter.project_slug}}/resources/logging_config.json
    cd ..

    git add .
    git commit -m "Application scaffold"
fi
