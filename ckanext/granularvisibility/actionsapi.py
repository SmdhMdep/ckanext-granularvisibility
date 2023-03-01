from ckan.plugins import toolkit
import ckan.model as model

import ckanext.granularvisibility.db as db

def get_package_visibility(context, data_dict):

    try: 
        data = {'id': data_dict['packageid']}

        packageInfo = toolkit.get_action('package_show')({'ignore_auth': True}, data)

        visibilityid = db.granular_visibility_mapping.get(packageid=packageInfo['id'])
        
        visibilityinfo = db.granular_visibility.get(visibilityid=visibilityid.visibilityid)
        if visibilityinfo is None:
            return "no visibility with name stated"

        return visibilityinfo
    except:
        return  "False"

def get_visibility_mapping(context, data_dict):

    data, errors = toolkit.navl_validate(
        data_dict,
        {"visibilityid": [toolkit.get_validator('ignore_empty'), str]},
    )

    visibilityinfo = db.granular_visibility.get(visibilityid=data['visibilityid'])
    if visibilityinfo is None:
        return "no visibility with name stated"

    return visibilityinfo.ckanmapping

def get_visibility(context, data_dict):

    data, errors = toolkit.navl_validate(
        data_dict,
        {"visibilityid": [toolkit.get_validator('ignore_empty'), str]},
    )

    visibilityinfo = db.granular_visibility.get(visibilityid=data['visibilityid'])
    if visibilityinfo is None:
        return "no visibility with name stated"

    return visibilityinfo

def add_visibility(context, data_dict):
    toolkit.check_access("isAdmin", context, data_dict)
    
    newVisibility = db.granular_visibility()
    if "visibility" not in data_dict:
        return False
    elif "ckanmapping" not in data_dict:
        return False
    elif "description" not in data_dict:
        return False

    data_dict['ckanmapping'] = bool(data_dict['ckanmapping'])

    newVisibility.visibility = data_dict['visibility']
    newVisibility.ckanmapping = data_dict['ckanmapping']
    newVisibility.description = data_dict['description']
    newVisibility.save()

    session = context['session']
    session.add(newVisibility)
    session.flush(newVisibility)
    session.refresh(newVisibility)
    visibilityinfo = newVisibility
    session.commit()

    return visibilityinfo

def delete_visibility_mapping(context, datasetID):

    visibility = db.granular_visibility_mapping.get(packageid=datasetID)
    
    if visibility is not None:
        session = context['session']
        session.delete(visibility)
        return True
    else:
        return False