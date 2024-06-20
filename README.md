# API server
> 클라이언트(앱)와 모델 서버를 중개하는 API 서버

## API Docs
[📌 API docs](http://43.201.117.55/docs)

### 1. GET `/models/adt/[init|min|max]-bound`
- 채점을 할 때, 연주의 delay를 고려하여 박자를 채점하기 위해 사용되는 상수값 GET API

![image](https://github.com/DoongDoongMaster/server/assets/68186101/a5ffae45-cddf-4891-897d-1acbaa74c18b)

### 2. POST `/models/adt/predict`
- 모델 서버에 ADT 모델 예측 요청을 보내는 API

![image](https://github.com/DoongDoongMaster/server/assets/68186101/cc028982-eedb-4ea0-ad09-fdee9bdfbeea)


### 3. POST `/models/omr/predict`
- 모델 서버에 OMR 모델 예측 요청을 보내는 API

![image](https://github.com/DoongDoongMaster/server/assets/68186101/f81e104c-ae9c-4f4b-860a-29fa6ff0ecd9)


<br><br>

## Preparation
- install docker engine
  ```shell
  # Add Docker's official GPG key:
  sudo apt-get update
  sudo apt-get install ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  
  # Add the repository to Apt sources:
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update

  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  ```
- install docker compose
  ```shell
  sudo apt-get update
  sudo apt-get install docker-compose-plugin
  ```

<br>

## Run
- 서버 실행 명령어
  - docker 컨테이너 띄워서 진행
  <br>
  
  ```shell
  docker compose up --build
  ```
  
