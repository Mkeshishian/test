from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pymysql

# Set up database connection
cnx = pymysql.connect(user='root', password='Blackops1871!',
                      host='127.0.0.1', database='recipes_db')
cursor = cnx.cursor()

# Set up Selenium
browser = webdriver.Chrome()
browser.get("https://www.allrecipes.com/recipes/76/appetizers-and-snacks/")

# Scroll down to load all recipes
elem = browser.find_element(By.TAG_NAME, "body")
no_of_pagedowns = 50
while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns -= 1

# Scrape recipe data and store in database
recipes = browser.find_elements(By.CSS_SELECTOR, ".component_card > .card__detailsContainer")
if len(recipes) == 0:
    print("Error: No recipes found!")
else:
    for recipe in recipes:
        title = recipe.find_element_by_css_selector(".card__title").text
        url = recipe.find_element_by_css_selector(".card__titleLink").get_attribute("href")
        try:
            rating = float(recipe.find_element_by_css_selector(".card__rating").get_attribute("data-ratingstars"))
        except:
            rating = None
        try:
            reviews = int(recipe.find_element_by_css_selector(".card__reviewCount").text\
                           .replace("(", "").replace(")", ""))
        except:
            reviews = None
        try:
            made_it_count = int(recipe.find_element_by_css_selector(".card__madeit").text\
                              .replace(",", ""))
        except:
            made_it_count = None
        insert_query = f"INSERT INTO recipes (title, url, rating, reviews, made_it_count) " \
                       f"VALUES ('{title}', '{url}', {rating}, {reviews}, {made_it_count})"
        cursor.execute(insert_query)

    # Commit changes and close database connection
    cnx.commit()
    cnx.close()

    # Close Selenium
    browser.close()
