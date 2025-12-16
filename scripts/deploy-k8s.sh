#!/bin/bash
echo "🚀 نشر Conscious Bridge Reloaded على Kubernetes"
kubectl apply -f k8s/
echo "✅ تم النشر"
echo "🔍 التحقق من الحالة:"
kubectl get pods
kubectl get services
