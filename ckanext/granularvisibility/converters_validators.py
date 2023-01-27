from ckan.plugins import toolkit
import ckanext.granularvisibility.actionsapi as action

import ckanext.granularvisibility.db as db

def set_ckan_visiability(key, data, errors, context):

    if ('visibilityid',) in data:
        data2 = {"visibilityid": data[('visibilityid',)]}

        visibilityRecord = db.granular_visibility_mapping.get(packageid=data[('id',)])

        if visibilityRecord is None:
            newVisibility = db.granular_visibility_mapping()
            newVisibility.visibilityid = data[('visibilityid',)]
            newVisibility.packageid = data[('id',)]
            newVisibility.save()

            session = context['session']
            session.add(newVisibility)
            session.commit()

        else:
            session = context['session']
            visibilityRecord.visibilityid = data[('visibilityid',)] 
            visibilityRecord.save()
            session.commit()

        ispublic = toolkit.get_action('get_visibility')({'ignore_auth': True}, data2)

        data[("private",)] = ispublic.ckanmapping

