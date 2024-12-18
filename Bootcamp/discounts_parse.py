import requests
from bs4 import BeautifulSoup

def find_discounts():
    games = []

    req = requests.get("https://store.steampowered.com/search/?specials=1")
    soup = BeautifulSoup(req.text, "html.parser")
    results = soup.find("div", id="search_resultsRows").find_all('a',class_='search_result_row ds_collapse_flag')

    for result in results:
        title = result.find("span", class_="title").text.strip()
        discount = ""
        if result.find("div", class_="discount_pct") is not None:
            discount = result.find("div", class_="discount_pct").text.strip()
        price = result.find("div", class_="discount_final_price").text.strip()
        link = result["href"]
        games.append({"title": title, "discount": discount, "price": price, "link": link})

    return games

if __name__ == "__main__":
    print(find_discounts())



