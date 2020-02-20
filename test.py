import requests
import stock_pull as pull
from enum import Enum
from bs4 import BeautifulSoup
import pprint


if __name__ == "__main__":
    pprint.pprint(pull.getIncomeStatement('fb'))