## Logstash Elasticsearch 6.x template

The default settings are to create one new index per day with five shards. This may result in too many shards, especially if log volume is low.

*Elasticseach 6.x compatibility notes*

+ _\_all_ is not permitted. Use _copy\_to_ if the functionality is required.
+ _\_default\__ mappings type is deprecated, because there can only be one type per index.
