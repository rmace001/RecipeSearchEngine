# RecipeSearchEngine
Search engine for recipes

## How to use Indexing scripts
1. Assuming you are starting from a fresh install of Ubuntu 18.04.5, run `./setup.sh` to install dependancies as well as Elasticserach
2. EDIT AND UNCOMMENT `network.host: 0.0.0.0` IN `/etc/elasticsearch/elasticsearch.yml`
3. Run `./run.sh` to create index by bulk-loading data, and run a simple query with the text, "chinese"
4. (optional) Run the multiline query commands
