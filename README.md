# be-api-reco-mvp

Flask API serving AI-based movie recommendations, taking in a movie title as input and providing similar movies as output.

The recommendation engine is a simple content based filtering algorithm trained on data from the [MovieLens dataset](https://grouplens.org/datasets/movielens/) using cosine similarity.

## Quick start

To test locally, run the different scripts inside of `/app/scripts` in order to train and test the model.

## Deployment

There is an AWS CodePipeline that will dockerize and deploy the server as an AWS Fargate task.