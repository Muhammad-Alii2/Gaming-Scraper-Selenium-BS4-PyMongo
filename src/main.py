from zestro import zestroRunAll
from xtreme import xtremeRunAll
from rbtech import rbtechRunAll
from czone import czoneRunAll
from jtech import jtechRunAll
from paklap import paklapRunAll


def run_all_scrapers():
    try:
        print("Running Zestro scraper...")
        zestroRunAll()  # Run the Zestro scraper
    except Exception as e:
        print(f"Error in Zestro scraper: {e}")

    try:
        print("Running Xtreme scraper...")
        xtremeRunAll()  # Run the Xtreme scraper
    except Exception as e:
        print(f"Error in Xtreme scraper: {e}")

    try:
        print("Running RBTech scraper...")
        rbtechRunAll()  # Run the RBTech scraper
    except Exception as e:
        print(f"Error in RBTech scraper: {e}")

    try:
        print("Running CZone scraper...")
        czoneRunAll()  # Run the CZone scraper
    except Exception as e:
        print(f"Error in CZone scraper: {e}")

    try:
        print("Running JTech scraper...")
        jtechRunAll()  # Run the JTech scraper
    except Exception as e:
        print(f"Error in JTech scraper: {e}")

    try:
        print("Running PakLap scraper...")
        paklapRunAll()  # Run the PakLap scraper
    except Exception as e:
        print(f"Error in PakLap scraper: {e}")


if __name__ == "__main__":
    run_all_scrapers()  # Execute the function to run all scrapers
