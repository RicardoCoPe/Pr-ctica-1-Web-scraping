from cars_scraper import scraping

if __name__ == '__main__':
    # Calling cars_scraper() function
    cars_df = scraping()

    # Write dataframe to a .csv file
    cars_df.to_csv('cars_dataset.csv', index=False)
