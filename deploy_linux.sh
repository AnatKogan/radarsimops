#!/usr/bin/env bash
set -e

echo "[1/4] Building Docker image (Linux)..."
docker build -t radarsimops:latest .

echo "[2/4] Applying Kubernetes manifests..."
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

echo "[3/4] Current pods:"
kubectl get pods

echo "[4/4] Current services:"
kubectl get svc

echo
echo "Try in browser:  http://localhost:30007/dashboard"
echo "Or curl:         curl http://localhost:30007/radar/status"
