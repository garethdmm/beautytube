from base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, PickleType, Text, or_, func

import json
import uuid
import datetime
import hashlib

from amazonproduct import *
from sqlalchemy.ext.declarative import declarative_base
from settings import settings
from session import get_a_session

metadata = Base.metadata

import json
import logging
logger = logging.getLogger(__name__)

class TextPickleType(PickleType):
    impl = Text


class SantaAmazonProduct(Base):
    __tablename__ = 'santa_amazon_product'

    amazon_product_id = Column(Integer, primary_key=True)

    description = Column(String(2018), nullable=False)
    image = Column(String(2018), nullable=False)
    title = Column(String(2018), nullable=False)
    price = Column(String(50), nullable=False)
    url = Column(String(2018), nullable=False)
    curated = Column(Boolean(False))
    keywords = Column(String(2018), nullable=True)
    product_type = Column(String(2018), nullable=True)
    product_metadata = Column(TextPickleType(pickler=json), nullable=True)
    
    def __init__(self, product, values={}, category='Generic'):
        if values:
            self.title = values.get('title')
            self.description = values.get('description')
            self.url = values.get('url')
            self.price = values.get('price')
            self.image = values.get('image')
            self.curated = values.get('curated')
            self.keywords = values.get('keywords')
            self.product_type = values.get('product_type')
            self.product_metadata = values.get('product_metadata')
            
        else:
            self.product_metadata = {}
            self.title = unicode(product.ItemAttributes.Title)
            try: 
                self.description = unicode(product.EditorialReviews.EditorialReview.Content)
            except AttributeError:
                self.description = ''

            try: 
                self.url = unicode(product.DetailPageURL)
            except AttributeError:
                self.url = ''

            try: 
                self.price = unicode(product.ItemAttributes.ListPrice.FormattedPrice)
                self.price = int(round(float(self.price.replace('$', ''))))
            except AttributeError:
                self.price = '$'

            try: 
                self.image = unicode(product.LargeImage.URL)
            
            except AttributeError:
                
                self.image = 'http://web.timesharejuice.com/Portals/108947/images/christmas-present1.jpg'
            
            try:
                self.product_type = unicode(product.ItemAttributes.ProductGroup)
            except AttributeError:
                self.product_type = ''

            try:
                if category == 'Books':
                    try:
                        self.author = unicode(product.ItemAttributes.Author)
                    except AttributeError:
                        self.author = ''

                    self.product_metadata['author'] = self.author

                elif category == 'DVD':
                    pass

                elif category == 'Music':
                    try:
                        self.artist = unicode(product.ItemAttributes.Artist)
                    except AttributeError:
                        self.artist = ''

                    self.product_metadata['artist'] = self.artist

            except AttributeError:
                self.product_metadata = {}
                
            self.product_metadata['category'] = category
            
                
    
    def __repr__(self):
        return json.dumps(self._as_dict())
    
    def __hash__(self):
      # the hash of our title is our unique hash
      return hash(self.title)
    
    def __cmp__(self, other):
      # similarly the strings are good for comparisons
      return cmp(self.title, other.title)
     
    def _as_dict(self):
        values = {
            'title': self.title, 
            'description': self.description ,
            'url': self.url ,
            'price': self.price ,
            'image': self.image ,
            'curated': self.curated,
            'keywords': self.keywords,
            'product_type': self.product_type,
            'product_metadata': self.product_metadata
        }
        return values
        
    @staticmethod
    def list_to_json(products):
        dict_products = []
        
        for product in products:
            dict_products.append(product.as_dict())

        return json.dumps(dict_products)
    
    
    @staticmethod
    def get_curated_products(category, page=1, num_per_page=10):
        session = get_a_session()
        page=int(page)
        num_per_page=int(num_per_page)
        products = session.query(SantaAmazonProduct).filter_by(curated=True).filter(or_(SantaAmazonProduct.keywords == category, SantaAmazonProduct.keywords == 'both' )).order_by(func.rand()).limit(num_per_page).all()
        return products

    @staticmethod
    def product_search(search_index='', Keywords='', ItemPage='', ResponseGroup='', return_top_results=1):

        param_key = hashlib.sha224('%r%r%r%r' % (search_index, Keywords, ItemPage, ResponseGroup)).hexdigest()
        

        if not settings['deployment'] == 'LOCALGARETH':
            existing_values = SantaAmazonProduct.get_from_memcache(param_key)

        else:
            existing_values = None
        if existing_values:
            
            try:
                return existing_values[return_top_results - 1:return_top_results]
            except:
                logging.info('There was less than %s pages' % return_top_results)
                return []
        else:
            
            products = []
            api = SantaAmazonProduct.amazon_api()
            try:
                pages = api.item_search(
                    search_index=search_index,
                    Keywords=Keywords,
                    ItemPage=ItemPage, 
                    ResponseGroup=ResponseGroup)
            except NoExactMatchesFound:
                logging.info('NoExactMatchesFound')
                return []
            except TooManyRequests:
                logging.info('TooManyRequests')
                return []
            
            
            x=0
            try:
                for page in pages:
                    for product in page.Items.Item:
                        x = x + 1
                        amazon_product = SantaAmazonProduct(product, category=search_index)
                        products.append(amazon_product)
                        if x >= 5:
                            break
                    break
            except Exception as e:
                logging.info(e)
                pass
            

            if not settings['deployment'] == 'LOCALGARETH':
                SantaAmazonProduct.save_product_list_to_memcache(param_key, products)        
            return products[return_top_results - 1:return_top_results]
    
    @staticmethod
    def save_product_list_to_memcache(key, products):
        from mc_session import mc
        existing_values = SantaAmazonProduct.get_from_memcache(key)
        
        if not existing_values:
            new_products_string_list = [repr(product) for product in products]
            mc.set(key, new_products_string_list)
        else:
            list_to_save = []
            existing_values.append(products)
            list_to_save = [repr(product) for product in existing_values]
            mc.set(key, list_to_save)
    
    def save_to_memcache(self, key):
        from mc_session import mc
        product = self
        existing_values = SantaAmazonProduct.get_from_memcache(key)

        if not existing_values:
            mc.set(key, [repr(product)])
        else:
            list_to_save = []
            existing_values.append(product)
            for product_in_list in existing_values:
                list_to_save.append(repr(product_in_list))
            mc.set(key, list_to_save)

    @staticmethod
    def get_from_memcache(key):
        from mc_session import mc
        product_string_list = mc.get(key)
        
        if product_string_list:
            product_list = []
            for product_string in product_string_list:
                product_dict = json.loads(product_string)
                product_list.append(SantaAmazonProduct(None, values=product_dict))
            return product_list  
        else:
            return None
    
    @staticmethod
    def amazon_api():
        return API(settings['aws_key'], settings['aws_secret_key'], 'us', associate_tag='sanssecapp-20')

    
