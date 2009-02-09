import index

store_dir = index.setupStorageDirectory() + '-test'

# search connection hub
searcher = index.search.IndexSearch(store_dir)

# async indexer 
indexer = index.xappy.IndexerConnection(store_dir)

# field definitions
index.setupFieldDefinitions(indexer)
