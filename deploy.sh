#!/bin/bash

# Deploy script for Cloud Run + Firebase Hosting
echo "Starting deployment..."

# Set your project variables
PROJECT_ID="cabw-black-electives-app"
SERVICE_NAME="cabw-elective-database"
REGION="us-central1"

# Check if gcloud CLI is installed
if ! command -v gcloud &> /dev/null; then
    echo "gcloud CLI not found. Please install it: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

# Set the project
echo "Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Build and deploy to Cloud Run
echo "Building and deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 300 \
  --set-env-vars SECRET_KEY="$(openssl rand -hex 32)"

# Deploy Firebase Hosting
echo "Deploying Firebase Hosting..."
firebase deploy --only hosting

echo "Deployment complete!"
echo "Cloud Run service: https://$SERVICE_NAME-$REGION.a.run.app"
echo "Firebase Hosting: https://$PROJECT_ID.web.app"