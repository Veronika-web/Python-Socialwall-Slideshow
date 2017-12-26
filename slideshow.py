#!/usr/bin/env python
#
#  Copyright (c) 2013, 2015, Corey Goldberg
#
#  Dev: https://github.com/cgoldberg/py-slideshow
#  License: GPLv3


import argparse
import random
import os

import pyglet
import json

import urllib.request
import urllib3

def update_pan_zoom_speeds():
    global _pan_speed_x
    global _pan_speed_y
    global _zoom_speed
    _pan_speed_x = random.randint(-8, 8)
    _pan_speed_y = random.randint(-8, 8)
    _zoom_speed = random.uniform(-0.02, 0.02)
    return _pan_speed_x, _pan_speed_y, _zoom_speed


def update_pan(dt):
    sprite.x += dt * _pan_speed_x
    sprite.y += dt * _pan_speed_y


def update_zoom(dt):
    sprite.scale += dt * _zoom_speed


def update_image(dt):
    img = pyglet.image.load(random.choice(image_paths))
    sprite.image = img
    sprite.scale = get_scale(window, img)
    sprite.x = 0
    sprite.y = 0
    update_pan_zoom_speeds()
    window.clear()


def get_image_paths(input_dir='.'):
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(('jpg', 'png', 'gif')):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)
    return paths


def get_scale(window, image):
    if image.width > image.height:
        scale = float(window.width) / image.width
    else:
        scale = float(window.height) / image.height
    return scale


window = pyglet.window.Window(fullscreen=True)


@window.event
def on_draw():
    sprite.draw()


if __name__ == '__main__':

    app_id = 'f0afca337586413cae1e68689d5f50b5'
    app_secret = 'abb10a6046d145b0be5e1d417a7f686b'
    base_api_url = 'https://www.socialmediawall.io/api/v1.1'
    wall_id = 12077
    limit = 10
    offset = 0
    
    address = '{}/{}/posts/?app_id={}&app_secret={}&limit={}&offset={}'.format(
                      base_api_url, 
                      wall_id, 
                      app_id, 
                      app_secret, 
                      limit, 
                      offset )
                      
    http = urllib3.PoolManager()
    response = http.request('GET', address)
    page = response.data
    result = json.loads(page)
    resultdata = result['data']
    if 'posts' in resultdata:
        for post in resultdata['posts']:
            try:
                print ('Downloading... ' + post['imagelink'])
                urllib.request.urlretrieve(post['imagelink'], "./images/{}.jpg".format(post['postid']))
                print ('Done')
            except Exception as e:
                print (e)
                pass
            
    _pan_speed_x, _pan_speed_y, _zoom_speed = update_pan_zoom_speeds()

    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory of images',
                        nargs='?', default=os.getcwd())
    args = parser.parse_args()

    image_paths = get_image_paths(args.dir)
    img = pyglet.image.load(random.choice(image_paths))
    sprite = pyglet.sprite.Sprite(img)
    sprite.scale = get_scale(window, img)

    pyglet.clock.schedule_interval(update_image, 6.0)
    pyglet.clock.schedule_interval(update_pan, 1/60.0)
    pyglet.clock.schedule_interval(update_zoom, 1/60.0)

    pyglet.app.run()
