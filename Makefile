# Docker の追加オプション
ifdef SIM_ENV_USE_TMPFS
DOCKER_MOUNT_DEV_SHM = -v /dev/shm:/tmp
endif

# make docker-build で Docker の初期化を行います
# クロスコンパイラをビルドし，Docker 内の /opt にインストールします
#
# make docker-run で，ホストのカレントディレクトリを Docker 内の /work にマウントして 
# Docker を起動します
USER_NAME = $(shell whoami)

# Docker コンテナ名
DOCKER_CONTAINER_NAME = $(USER_NAME)-sim-env

# Docker イメージの実行
# -v $(HOME):$(HOME) 							実行しているユーザの HOME をそのままコンテナ内にマウント
# -e ENTRY_POINT_PATH=$(PWD) 					起動時の初期パスを渡す
# -e USER_ID=$(shell id -u) -e GROUP_ID=$(shell id -g) -e USER_NAME=$(USER) 	ユーザー情報を渡す
# -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix 	X11 アプリを起動するための設定
# -v /dev/shm:/tmp 								ホストの /dev/shm を /tmp にマウント
DOCKER_COMMAND = \
	docker run -ti --rm \
	-v $(HOME):$(HOME) \
	-e ENTRY_POINT_PATH=$(PWD) \
	-e USER_ID=$(shell id -u) -e GROUP_ID=$(shell id -g) -e USER_NAME=$(USER) \
	-e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
	$(DOCKER_MOUNT_DEV_SHM) \
	$(DOCKER_CONTAINER_NAME):latest 


# Docker コンテナを初期化
docker-build:
	docker build -t $(DOCKER_CONTAINER_NAME) .

# Docker 内シェルに入る
docker-run:
	@$(DOCKER_COMMAND) 

# 使用する際は事前に docker グループに自身を追加しておいてください
docker-add-user:
	sudo usermod -aG docker $(USER_NAME)
