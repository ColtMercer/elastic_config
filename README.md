# elastic_config
Project to explore using ElasticSearch for scalable text search. Data set is the Stephen King booked downloaded from Kaggle. The purpose is to test the performance of ElasticSearch API for text search to simulate Network Config search.
https://www.kaggle.com/datasets/lujar1762/stephen-king-books

## Setup
```bash
docker-compose up -d
```

## Troubleshooting
If data is not created, check the logs of the data_creator container. It may be that the data is not being created because the elasticsearch container is not ready yet. In that case, restart the data_creator container.