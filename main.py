# -*- coding: utf-8 -*-
# Module: default
# Author: PeterBY
# Created on: 06.11.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import os
import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

mode = args.get('mode', None)


# Simple URL builder
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


_resources_path = os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources')


def get_image(filename):
    return os.path.join(_resources_path, 'images', filename)


# Add more shows here:
_shows = [
    {'name': 'Вечерний Ургант', 'show_id': '41', 'poster': get_image('urgant.jpg')},
    {'name': 'Смак', 'show_id': '116', 'poster': get_image('smak.jpg')},
    {'name': 'Контрольная закупка', 'show_id': '78', 'poster': get_image('zakupka.jpg')},
	{'name': 'Модный приговор', 'show_id': '87', 'poster': get_image('prigovor.jpg')},
    {'name': 'Непутевые заметки', 'show_id': '99', 'poster': get_image('zametki.jpg')},
    {'name': 'Жить здорово!', 'show_id': '68', 'poster': get_image('zdorovo.jpg')},
    {'name': 'Здоровье', 'show_id': '71', 'poster': get_image('zdorovie.jpg')},
    {'name': 'Таблетка', 'show_id': '486', 'poster': get_image('tabletka.jpg')},
    {'name': 'На 10 лет моложе', 'show_id': '337', 'poster': get_image('molozhe.jpg')},
    {'name': 'Теория заговора', 'show_id': '627', 'poster': get_image('zagovor.png')},
    {'name': 'Познер', 'show_id': '106', 'poster': get_image('pozner.jpg')},
    {'name': 'Фазенда', 'show_id': '139', 'poster': get_image('fazenda.png')},
    {'name': 'Давай поженимся!', 'show_id': '626', 'poster': get_image('davai.jpg')},
    {'name': 'Без страховки', 'show_id': '494', 'poster': get_image('strahovki.jpg')},
    {'name': 'Концерты', 'show_id': '234', 'poster': get_image('koncerty.jpg')},
    {'name': 'Точь-в-точь', 'show_id': '767', 'poster': get_image('toch.jpg')},
    {'name': 'Что? Где? Когда?', 'show_id': '147', 'poster': get_image('kogda.jpg')},
    {'name': 'Путешествия Познера и Урганта', 'show_id': '513', 'poster': get_image('pozner-urgant.jpg')}
]


# Create a list episodes of show
def get_videos(show_id, index):
    videos = []
    json = requests.get(
        'http://www.1tv.ru/video_materials.json?collection_id={0}&index={1}'.format(show_id, index * 50)).json()
    for element in json:
        videos.append({'title': element['title'], 'src': 'http:' + element['mbr'][0]['src'],
                       'poster': 'http:' + element['poster']})
    return videos


def list_shows():
    """
    Create the list of shows in the Kodi interface.

    """
    # Create a list for our items.
    listing = []
    # Iterate through shows.
    for show in _shows:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(show['name'])
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # http://mirrors.xbmc.org/docs/python-docs/16.x-jarvis/xbmcgui.html#ListItem-setArt
        list_item.setArt({'poster': show['poster'], 'fanart': show['poster']})
        # Set additional info for the list item.
        # http://mirrors.xbmc.org/docs/python-docs/16.x-jarvis/xbmcgui.html#ListItem-setInfo
        # list_item.setInfo('video', {'title': category})
        # Create a URL for the plugin recursive callback.
        url = build_url({'mode': 'folder', 'show_name': show['name'], 'show_id': show['show_id'], 'index': '0'})
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))

    # # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    # xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(addon_handle)


def list_videos(show_name, show_id, index):
    """
    Create the list of playable videos in the Kodi interface.

    """
    # Add "more" link
    url_next = build_url({'mode': 'folder', 'show_name': show_name, 'show_id': show_id, 'index': index + 1})
    li_next = xbmcgui.ListItem('Страница № ' + str(index + 1) + '. Следующая...', iconImage=get_image('next.png'))
    xbmcplugin.addDirectoryItem(addon_handle, url_next, li_next, isFolder=True)
    # Get the list of videos for the show.
    videos = get_videos(show_id, index)
    # Create a list for our items.
    listing = []
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(video['title'])
        # Set additional info for the list item.
        list_item.setInfo('video', {'title': video['title']})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'poster': video['poster'], 'fanart': video['poster']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for the plugin recursive callback(just link source).
        url = video['src']
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))
    # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
    # Add "more" link
    xbmcplugin.addDirectoryItem(addon_handle, url_next, li_next, isFolder=True)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    # xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(addon_handle)


if mode is None:
    list_shows()

elif mode[0] == 'folder':
    _show_name = args['show_name'][0]
    _show_id = args['show_id'][0]
    _index = int(args['index'][0])
    list_videos(_show_name, _show_id, _index)
