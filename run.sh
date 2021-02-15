#!/usr/bin/env bash
# Start Elasticsearch
sudo /bin/systemctl daemon-reload && \
sudo /bin/systemctl enable elasticsearch.service && \
sudo /bin/systemctl start elasticsearch.service && \

# Check Elasticsearch
curl 127.0.0.1:9200 && \
# Index data
curl -H 'Content-Type: application/json' -X POST 'localhost:9200/recipes/doc/_bulk?pretty' --data-binary @ofile.json && \
# View indices
curl -X GET 127.0.0.1:9200/_cat/indices?v && \
# Ugly search
curl -X GET localhost:9200/_search?q=chinese
# 
# Pretty search: can uncomment and copy/paste the 8 lines to prompt
# curl -H "Content-Type: application/json" -XGET '127.0.0.1:9200/recipes/_search?pretty' -d '
# {
#     "query": {
#     "query_string" : {
#     "query" : "wok"
# }
# }
# }' > out.json
# 
# 
# # Query field (haven't figured out activeTime query)
# curl -H "Content-Type: application/json" -XGET '127.0.0.1:9200/recipes/_search?pretty' -d '
# {
#     "query": {
#     "term" : {
#     "specialEquipment" : "wok"
# }
# }
# }' > out.json
