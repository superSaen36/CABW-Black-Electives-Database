gcloud builds submit --tag gcr.io/black-electives-database/black-electives-app 

gcloud run deploy --image gcr.io/black-electives-database/black-electives-app --region us-west1 --platform managed --allow-unauthenticated --port 8080