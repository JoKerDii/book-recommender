from dotenv import load_dotenv
import requests
import os

load_dotenv()
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

def search_books(query, max_results=5):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query,
        "maxResults": max_results,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        books = []
        for item in data.get("items", []):
            volume_info = item.get("volumeInfo", {})
            books.append({
                "title": volume_info.get("title"),
                "authors": volume_info.get("authors"),
                "description": volume_info.get("description"),
                "averageRating": volume_info.get("averageRating"),
                "categories": volume_info.get("categories"),
                "infoLink": volume_info.get("infoLink"),
            })
        return books
    else:
        raise Exception(f"Failed to fetch books: {response.status_code}")
    
if __name__ == "__main__":

    print(search_books('daring greatly'))