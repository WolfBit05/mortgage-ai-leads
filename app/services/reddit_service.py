from app.scraper.reddit import scrape_reddit


def run():
    print("Starting Reddit pipeline...")

    scrape_reddit()

    print("Pipeline completed.")