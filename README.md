gcloud builds submit --tag gcr.io/globalwarming-392019/GlobalWarming  --project=globalwarming-392019

gcloud run deploy --image gcr.io/globalwarming-392019/GlobalWarming --platform managed  --project=globalwarming-392019 --allow-unauthenticated