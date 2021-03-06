#!/usr/bin/env python
# coding: utf-8
import requests
import time
from bs4 import BeautifulSoup
from datetime import date

# Request newegg data
newegg_url = 'https://www.newegg.com/p/pl?N=100007709%204814&page='
page_size = '&PageSize=96'
filename = './csv_files/newegg_GPU_' + str(date.today()) + '.csv' 
file = open(filename, 'w')

# header = 'Date, Product_name, Producer, Price, Shipping, Rating, Number of Ratings\n'
header = 'Brand,Series,Model,Interface,Chipset Manufacturer,GPU Series,GPU,Core Clock,Boost Clock,Effective Memory Clock,Memory Size,Memory Interface,Memory Type,DirectX,OpenGL,HDMI,DisplayPort,Max Resolution,SLI Support,Thermal Design Power,Date First Available'
file.write(header + '\n')
# loop over many pages, about 10, max is about 27 pages
for j in range(1, 28):
    r = requests.get(newegg_url + str(j) + page_size)
    newegg_html = r.text
    # Clean html data
    newegg_soup = BeautifulSoup(newegg_html, 'html.parser')
    pretty_newegg_soup = newegg_soup.prettify()
    # get list of video cards
    vCard_list = newegg_soup.findAll('div', {'class':'item-container'})
    for i in range(len(vCard_list)):
        # get video card name and brand
        vCard = vCard_list[i]
        vCard_title = vCard.findAll('a', {'class':'item-title'})
        try:
            if len(vCard_title):
                vCard_name = vCard_title[0].text.split(' ', 1)[1]
                vCard_brand = vCard_title[0].text.split(' ')[0]
            else:
                vCard_img = vCard.findAll('a', {'class':'item-brand'})
                if len(vCard_img) and str(vCard_img[0]).find('title='):
                    vCard_brand = str(vCard_img[0])[x+7:x+18]
                else:
                    vCard_name = ''
                    vCard_brand = ''
        except:
            vCard_name = ''
            vCard_brand = ''
            
        # get product ratings
        vCard_rating = vCard.findAll('a', {'class':'item-rating'})
        try:
            if len(vCard_rating) and str(vCard_rating[0]).find('title='):
                x = str(vCard_rating[0]).find('title=')
                vCard_rate5 = str(vCard_rating[0])[x+7:x+18]
                vCard_n_ratings = str(vCard_rating[0].span.text).strip('()')
        except:
            vCard_rate5 = ''
            vCard_n_ratings = ''
    
        # get product price
        vCard_cost = vCard.findAll('li', {'class':'price-current'})
        vCard_shipping = vCard.findAll('li', {'class':'price-ship'})
        try:
            if len(vCard_cost):
                vCard_price = vCard_cost[0].strong.text
            if len(vCard_shipping):
                vCard_ship_price = vCard_shipping[0].text.strip()
        except:
            vCard_price = ''
            vCard_ship_price = ''

        file.write(str(date.today()) + ';' + vCard_name.replace(';', '') + ';' + vCard_brand + ';' 
                   + vCard_price + ';' + vCard_ship_price + ';' + vCard_rate5 + ';' + vCard_n_ratings + '\n')
    time.sleep(10)
file.close()

