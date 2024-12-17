import requests

def fetch_anime_by_genre(genre):
    query = """
    query ($genres: [String]) {
    Page {
        media(genre_in: $genres, type: ANIME) {
        id
        title {
            romaji
            english
            native
        }
        status
        genres
        popularity
        }
    }
    }
    """
    # Define query variables
    variables = {"genre_in": genre}
    url = "https://graphql.anilist.co"

    try:
        # Send the POST request
        response = requests.post(url, json={"query": query, "variables": variables})
        response.raise_for_status()  # Raise an error for HTTP issues
        # Parse the JSON response
        return response.json()  # Return the data
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def fetch_anime_by_title(anime_title):
    query = """
    query ($search: String!) {
    Page {
        media(search: $search, type: ANIME) {
        id
        title {
            romaji
            english
            native
        }
        status
        genres
        seasonYear
        popularity
        averageScore
        countryOfOrigin	
        episodes
        seasonYear
        }
        }
    }
    }
    """
    # Define query variables
    variables = {"search": anime_title}
    url = "https://graphql.anilist.co"

    try:
        # Send the POST request
        response = requests.post(url, json={"query": query, "variables": variables})
        response.raise_for_status()  # Raise an error for HTTP issues
        # Parse the JSON response
        return response.json()  # Return the data
    except requests.exceptions.RequestException as e:
        print(e)
        return None
