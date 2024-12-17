# Copyright (c) 2024 Artur Cherchenko
#
# All Rights Reserved.
#
# This software and associated documentation files (the "Software") are provided for personal
# and non-commercial use only. Permission is granted to use, copy, and modify the Software
# for non-commercial purposes, provided that the following conditions are met:
#
# 1. The above copyright notice and this permission notice shall be included in all copies
#    or substantial portions of the Software.
#
# 2. Proper credit must be given to the original author, Artur Cherchenko, in any project,
#    documentation, or distribution that uses this Software.
#
# 3. Commercial use, including but not limited to selling, licensing, or using the Software
#    in any project or product for financial gain, is strictly prohibited without prior written
#    consent and a separate commercial license agreement from the author.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR
# OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import requests
from api import fetch_anime_by_genre, fetch_anime_by_title

# source venv/bin/activate


def main():
    anime_title = get_anime_title()  # Get anime title from user input
    data = fetch_anime_by_title(anime_title)  # Fetch anime details by title
    selected_anime = display_and_choose_anime(data)  # Prompt user to select an anime
    print_the_original_list(selected_anime)  # Print the details of the selected anime

    # Genre exploration
    genre_list = explore_anime_by_genre(
        selected_anime
    )  # Ask user if they want recommendations
    if genre_list:  # Proceed only if genres are provided
        fetched_genres = fetch_anime_by_genre(
            genre_list
        )  # Fetch recommendations by genre
        print("\nRecommendations based on genre:")
        display_genre_recommendations(
            fetched_genres
        )  # Display recommendations without prompting


def print_the_recomendation_list(recomendations):
    print(recomendations)


def print_the_original_list(selected_anime):
    if selected_anime:
        print("\nYou selected:")
        print_anime_details(selected_anime)
    else:
        print("Failed to fetch anime details.")


def get_anime_title():
    return input("What's the title of the anime you would like to search? ").strip()


def display_and_choose_anime(data):
    media_list = data.get("data", {}).get("Page", {}).get("media", [])
    if not media_list:
        print("No matching anime found.")
        return
    for index, media in enumerate(media_list, start=1):
        anime_id = media.get("id", "Unknown ID")
        title = media.get("title", {}).get("english", "Unknow Title")
        status = media.get("status", "Unknown Status")
        genre = ", ".join(media.get("genres", []))
        season_year = media.get("seasonYear", {})
        # If the english title is unavailable it takes a romaji title instead
        if title == None:
            title = media.get("title", {}).get("romaji", "Unknow Title")
        print(
            f"{index} | ID: {anime_id}, Title: {title}, Status: {status}, Genre: {genre}, Year Released: {season_year}"
        )
    while True:
        try:
            choice = int(
                input(
                    "Enter the number of the anime you would like to learn more about: "
                )
            )
            if 1 <= choice <= len(media_list):
                return media_list[choice - 1]
            else:
                print("Invalid Selection")
        except ValueError:
            print("Please enter a valid number")


def print_anime_details(anime):
    anime_id = anime.get("id", "Unknown ID")
    title = anime.get("title", {}).get("english", "Unknown Title")
    romaji = anime.get("title", {}).get("romaji", "Unknown Romaji Title")
    native = anime.get("title", {}).get("native", "Unknown Native Title")
    status = anime.get("status", "Unknown Status")
    season_year = anime.get("seasonYear", {})
    popularity = anime.get("popularity", "No popularity data available ")
    average_score = anime.get("averageScore", "No Score")
    amount_of_episodes = anime.get("episodes", "")
    country_origin = anime.get("countryOfOrigin", "Unknown Origin")
    genre = ", ".join(anime.get("genres", []))

    print(f"ID: {anime_id}")
    print(f"Title (English): {title}")
    print(f"Title (Romaji): {romaji}")
    print(f"Title (Native): {native}")
    print(f"Status: {status}")
    print(f"Episodes: {amount_of_episodes}")
    print(f"Year Released: {season_year}")
    print(f"Popularity: {popularity}")
    print(f"Country Of Origin: {country_origin}")
    print(f"Average Score: {average_score}")
    print(f"Genre: {genre}", end="\n" * 2)


def display_genre_recommendations(data):

    # Extract the list of media from the API response
    media_list = data.get("data", {}).get("Page", {}).get("media", [])

    # Check if the list is empty
    if not media_list:
        print("No recommendations found.")
        return  # Exit the function if no media is found

    # Iterate through the list and print each anime's details
    for index, anime in enumerate(media_list, start=1):
        anime_id = anime.get("id", "Unknown ID")
        title = anime.get("title", {}).get("english", "Unknow Title")
        status = anime.get("status", "Unknown Status")
        genre = ", ".join(anime.get("genres", []))
        print(
            f"{index} | ID: {anime_id}, Title: {title}, Status: {status}, Genre: {genre}"
        )


# This functions finds anime that have 1 or more same genres
def explore_anime_by_genre(genre):
    while True:
        would_like_to_explore = (
            input(
                "Would you like to get more anime recomendations based on last animes search? (y/n) "
            )
            .strip()
            .lower()
        )
        if would_like_to_explore == "y":
            genre_list = genre.get("genres", [])
            return genre_list
        elif would_like_to_explore == "n":
            break


if __name__ == "__main__":
    main()
