#!/bin/bash

# Deploy script for Firebase Functions
echo "Starting Firebase deployment..."

# Install Firebase CLI dependencies
echo "Installing dependencies..."
npm install

# Install Python dependencies for Functions
echo "Installing Python dependencies..."
cd functions
pip install -r requirements.txt
cd ..

# Deploy to Firebase
echo "Deploying to Firebase..."
npx firebase deploy

echo "Deployment complete!"