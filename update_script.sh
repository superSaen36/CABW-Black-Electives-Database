#!/bin/bash

gcloud config set project cabw-black-electives-app

gcloud run deploy cabw-elective-database \
    --source . \
    --platform managed \
    --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 300

# Deploy Firebase Hosting
firebase deploy --only hosting