#!/bin/bash
set -Ceufox pipefail

if [[ -z "${BEARHUB_VERSION:-}" ]]; then
  echo "Set BEARHUB_VERSION to a Bearhub release tag (e.g. 0.10.7-bearhub.6)." >&2
  exit 1
fi

docker build -t bearhub-appimage .
docker run -e BEARHUB_VERSION="$BEARHUB_VERSION" -v ./AppImageBuilder.yml:/build/AppImageBuilder.yml --rm --cap-add=SYS_ADMIN --device /dev/fuse --mount type=bind,source="$(pwd)",target=/build bearhub-appimage
# volume required to run tests: -v /var/run/docker.sock:/var/run/docker.sock