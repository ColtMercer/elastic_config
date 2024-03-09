import requests
import elasticsearch


# Create function to search Elasticsearch for book content using regex patters
def search_elastic(pattern: str) -> list[dict]:
    ''' Search Elasticsearch for book titles using regex patterns
    Args:
        pattern str: regex patterns to search for
    Returns:
        list[dict]: List of books that match the regex pattern and the text matches
    '''
    # Search Elasticsearch
    client = elasticsearch.Elasticsearch('http://localhost:9200')
    response = client.search(
        index='stephen_king',
        body={
            'query': {
                'regexp': {
                    'contents': pattern
                }
            }
        }
    )

    # Return the hits
    return response['hits']['hits']


if __name__ == '__main__':
    # Search for the word "guns"
    results = search_elastic('guns')
    for result in results:
        print(result['_source']['title'])
        print(result['_source']['contents'])
        print()

