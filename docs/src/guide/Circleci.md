## Deployment of Onsite Health Diagnostic website

After integrating the backend and testing the application the final part left is deploying of the complete application to the cloud platform so that user can use our website anywhere in the world.<br>
For deploying the complete application the tools we used here are `circle-ci` for building CI/CD pipeline,`Docker` for Contenarization and `Heroku` for cloud hosting .For the automation of the project we have applied **Mlops** strategy i.e Machine learning operations for deploying our complete application in the automated way.
<br>
Now we will explain how we will explain about creating CI/CD pipeline using circle-ci
<br>
#### Create a file "Dockerfile" with below content
```
FROM python:3.7
COPY ./app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["main.py"]
```

#### Create a "Procfile" with following content

`web:gunicorn main:app $PORT`

#### create a file ".circleci\config.yml" with following content
```
version: 2.1
orbs:
  heroku: circleci/heroku@1.0.1                                                                  
jobs:                                                  
  build-and-test:
    executor: heroku/default
    docker:
      - image: circleci/python:3.6.2-stretch-browsers
        auth:
          username: mydockerhub-user
          password: $DOCKERHUB_PASSWORD  # context / project UI env-var reference
    steps:
      - checkout
      - restore_cache:
          key: deps1-{{ .Branch }}-{{ checksum "requirements.txt" }}
      - run:
          name: Install Python deps in a venv
          command: |
            echo 'export TAG=0.1.${CIRCLE_BUILD_NUM}' >> $BASH_ENV
            echo 'export IMAGE_NAME=python-circleci-docker' >> $BASH_ENV
            python3 -m venv venv
            . venv/bin/activate
            pip install --upgrade pip
            pip install -r requirements.txt
      - save_cache:
          key: deps1-{{ .Branch }}-{{ checksum "requirements.txt" }}
          paths:
            - "venv"
      - run:
          command: |
            . venv/bin/activate
            python -m pytest -v test/test.py
      - store_artifacts:
          path: test-reports/
          destination: tr1
      - store_test_results:
          path: test-reports/
      - setup_remote_docker:
          version: 19.03.13
      - run:
          name: Build and push Docker image
          command: |
            docker build -t $DOCKERHUB_USER/$IMAGE_NAME:$TAG .
            docker login -u $DOCKERHUB_USER -p $DOCKER_HUB_PASSWORD_USER docker.io
            docker push $DOCKERHUB_USER/$IMAGE_NAME:$TAG
  deploy:
    executor: heroku/default
    steps:
      - checkout
      - run:
          name: Storing previous commit
          command: |
            git rev-parse HEAD > ./commit.txt
      - heroku/install
      - setup_remote_docker:
          version: 18.06.0-ce
      - run:
          name: Pushing to heroku registry
          command: |
            heroku container:login
            #heroku ps:scale web=1 -a $HEROKU_APP_NAME
            heroku container:push web -a $HEROKU_APP_NAME
            heroku container:release web -a $HEROKU_APP_NAME

workflows:
  build-test-deploy:
    jobs:
      - build-and-test
      - deploy:
          requires:
            - build-and-test
          filters:
            branches:
              only:
                - main
  ```               
#### Replicate the requirements.txt file to your local node 
`pip freeze > requirements.txt`

#### initialize git repo
```
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin <github_url>
git push -u origin main
```

#### create a account at circle ci
https://circleci.com/login/

#### create an account at heroku
https://id.heroku.com/login

#### Create api authenticated key at heroku
Go to `Heroku Profile Page` and then click on navaigation bar named `applications` and then click on `create authrization` finally enter `description` and then you will be able to generate API key.

#### create a account at docker hub
https://hub.docker.com/login

#### Setup project
https://app.circleci.com/projects/github/Avnish327030/setup/

#### Select project setting in CircleCI and below environment variable
```
DOCKERHUB_USER
DOCKER_HUB_PASSWORD_USER
HEROKU_API_KEY
HEROKU_APP_NAME
HEROKU_EMAIL_ADDRESS
DOCKER_IMAGE_NAME= <any random name starting with char ending with int64> eg:onsite1234
```

#### To update the modification
```
git add .
git commit -m "proper message"
git push
```

### THATS IT KUDOS SUCCESSFULLY MADE AUTOMATED DEPLOYMENT USING CIRCLE-CI PIPELINE
