from typing import Iterable

import scrapy
from ..items import PeriodicElementItem
from scrapy.loader import ItemLoader
from scrapy import Request


class PeriodicElementsSpider(scrapy.Spider):
    name = "periodic_elements"
    def start_requests(self):
        yield scrapy.Request("https://pubchem.ncbi.nlm.nih.gov/ptable/", meta=dict(playwright=True))

    def parse(self, response):
        for element in response.css("div.ptable div.element"):
            i = ItemLoader(item=PeriodicElementItem(), selector=element)

            i.add_css("name", "[data-tooltip='Name']")
            i.add_css("symbol", "[data-tooltip='Symbol']")
            i.add_css("atomic_mass", "[data-tooltip='Atomic Mass, u']")
            i.add_css("atomic_numb", "[data-tooltip='Atomic Number']")
            i.add_css("chemical_group", "[data-tooltip='Chemical Group Block'] span")

            yield i.load_item()