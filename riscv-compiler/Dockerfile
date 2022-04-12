#FROM ubuntu:20.04
FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND noninteractive
ENV GIT_SSL_NO_VERIFY 1

# python3 is necessary to build gcc
RUN apt-get update && \
    apt-get install tzdata -y && \
    apt-get install --no-install-recommends -y \
        autoconf automake autotools-dev curl \
        libmpc-dev libmpfr-dev libgmp-dev \
        gawk build-essential bison flex texinfo \
        gperf libtool patchutils bc zlib1g-dev libexpat-dev gosu \
        git python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG WORK_PATH=/work
ARG TMP_PATH=/build-work


COPY Makefile ${TMP_PATH}/

# These variables are referred in Makefile
# refs/tags/2021.09.21 is gcc ver 11.1
ENV SIM_ENV_GCC_PREFIX_BASE /usr/local
ENV RISCV64_LINUX_GCC_PATH /usr/local
ENV RISCV64_LINUX_GCC_TAG refs/tags/2021.09.21
ENV RISCV64_ELF_GCC_PATH /usr/local
ENV RISCV64_ELF_GCC_TAG refs/tags/2021.09.21
ENV RISCV32LINUX_GCC_PATH /usr/local
ENV RISCV32_LINUX_GCC_TAG refs/tags/2021.09.21
ENV RISCV32_ELF_GCC_PATH /usr/local
ENV RISCV32_ELF_GCC_TAG refs/tags/2021.09.21

RUN \
    cd ${TMP_PATH} && \
    make clone && \
    make build_riscv64_linux -j"$(nproc)" && make clean && \
    make build_riscv32_linux -j"$(nproc)" && make clean && \
    make build_riscv64_elf -j"$(nproc)" && make clean && \
    make build_riscv32_elf -j"$(nproc)" && make clean && \
    rm ${TMP_PATH} -f -r

# Set root password
RUN echo "root:root" | chpasswd

# Create an user
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Set the entry point
# "entrypoint.sh" changes a user ID dynamically.
# If no additional commands are not passed, /bin/bash is launched.
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/bin/bash"]

# Set a work directory
WORKDIR ${WORK_PATH}

