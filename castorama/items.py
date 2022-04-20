import scrapy
from itemloaders.processors import Compose, MapCompose, TakeFirst


def convert_price(value):
    value = value.replace('\xa0', '')
    value = value.replace(' ', '')
    try:
        value = int(value)
    except:
        return value
    return value


def parse_value(data):
    for num, elem in enumerate(data):
        elem = elem.strip()
        data[num] = elem
    return data


class CastoramaItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(convert_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field()
