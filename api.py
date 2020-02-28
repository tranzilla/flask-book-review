import requests
def main():
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "ulMNEp286MNXSAY7WZYVA", "isbns": "0380795272"})
    data = res.json()
    average_rating = data["books"][0]["average_rating"]
    print(f"The average_rating for the book is {average_rating}")

if __name__ == '__main__':
    main()
