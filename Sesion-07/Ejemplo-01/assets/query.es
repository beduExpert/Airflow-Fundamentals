/* http://0.0.0.0:9200 */
GET /_cluster/health

POST /catalog/_doc/1001
{
    "title": "Java 8 Optional In Depth",
    "category": "Java",
    "published_date": "23-FEB-2017",
    "author": "Rambabu Posa"
}
POST /catalog/_doc/1002
{
  "title": "Elastic Search Basics",
  "category":"ElasticSearch",
  "published_date":"03-MAR-2017",
  "author":"Rambabu Posa"
}
POST /catalog/_doc/1003
{
  "title": "Spring + Spring Data + ElasticSearch",
  "category":"Spring",
  "published_date":"11-MAR-2017",
  "author":"Rambabu Posa"
}
POST /catalog/_doc/1004
{
  "title": "Spring + Spring Data + ElasticSearch",
  "category":"Spring Boot",
  "published_date":"23-MAR-2017",
  "author":"Rambabu Posa"
}

get /catalog/_doc/1005
