#!/bin/bash

set -e

# CONFIG
NAMESPACE="{{docker-hub-username}}"
IMAGE_NAME="{{repo-name}}"
INCREMENT="patch"  # patch | minor | major

REPO="$NAMESPACE/$IMAGE_NAME"

echo "Fetching latest version from Docker Hub..."

LATEST_TAG=$(curl -s "https://registry.hub.docker.com/v2/repositories/$REPO/tags?page_size=100" \
  | jq -r '.results[].name' \
  | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' \
  | sort -V \
  | tail -n 1)

if [ -z "$LATEST_TAG" ]; then
  echo "No version found. Defaulting to 0.0.0"
  LATEST_TAG="0.0.0"
fi

echo "Latest version: $LATEST_TAG"

IFS='.' read -r MAJOR MINOR PATCH <<< "$LATEST_TAG"

case "$INCREMENT" in
  major)
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
  minor)
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
  patch)
    PATCH=$((PATCH + 1))
    ;;
  *)
    echo "Invalid increment type"
    exit 1
    ;;
esac

NEW_TAG="$MAJOR.$MINOR.$PATCH"

echo "New version: $NEW_TAG"

echo "Building image..."
docker build -t "$REPO:$NEW_TAG" -t "$REPO:latest" .

echo "Pushing image..."
echo "$REPO:$NEW_TAG"
docker push "$REPO:$NEW_TAG"
docker push "$REPO:latest"

echo "✅ Published $REPO:$NEW_TAG"
