from __future__ import absolute_import

from ckan.plugins import toolkit

import ckanext.granularvisibility.db as db

import sqlalchemy as sa

c = toolkit.c

def get_visibilities():
    visibilityinfo = db.granular_visibility.get_all()

    #TODO: add error if no get_visibilities

    # Used to add new visibilities during testing
    #data = {'visibility': "Private User Shareable",'ckanmapping': True, 'description': "This dataset can only be seen by members of your organization but also allows you to create a list of allowed users that can also see and download the dataset"}
    #toolkit.get_action('add_visibility')({'ignore_auth': True}, data)

    visibilitylist = []

    try:
        for x in visibilityinfo:
            visibilitylist.append(x)
    except:
        visibilitylist.append(visibilityinfo)

    return visibilitylist

def is_selected(packageid, visibilityid):

    data = {'packageid': packageid}

    visibility = toolkit.get_action('get_package_visibility')({'ignore_auth': True}, data)

    try:
        if visibility.visibilityid == visibilityid:
            return True
        else:
            return False
    except:
        return False