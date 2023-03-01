import ckan.model as model
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from flask import Blueprint

import ckanext.granularvisibility.actionsapi as actionsapi
import ckanext.granularvisibility.helpers as helpers
import ckanext.granularvisibility.auth as auth
import ckanext.granularvisibility.db as db

c = toolkit.c

# Used to add page in later get_blueprint()
def visibility_show():
    context = {'model': model, 'user': c.user, 'auth_user_obj': c.userobj}
    try:
        toolkit.check_access('sysadmin', context, {})
        return toolkit.render('admin/addVisibility.html')
    except toolkit.NotAuthorized:
        return toolkit.abort(403, 'Need to be system administrator to administer')

class GranularvisibilityPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IPackageController , inherit=True)

    # IConfigurable
    # Creates DB table
    def configure(self, config):
        if not db.granular_visibility_mapping_table.exists():
            db.granular_visibility_mapping_table.create()
        if not db.granular_visibility_table.exists():
            db.granular_visibility_table.create()

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'granularvisibility')

    # IDatasetForm
    def _modify_package_schema(self, schema):
        schema.update({
                'visibilityid': [
                    toolkit.get_validator('ignore_missing')
                ]
            })
        return schema

    def show_package_schema(self):
        schema = super(GranularvisibilityPlugin, self).show_package_schema()
        schema = self._modify_package_schema(schema)
        return schema 

    def create_package_schema(self):
        schema = super(GranularvisibilityPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(GranularvisibilityPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def after_create(self, context, pkg_dict):
        print("RRRRRRRRRRRRRRRRR ", pkg_dict["id"])

        if 'visibilityid' in pkg_dict and 'id' in pkg_dict:
            visibilityRecord = db.granular_visibility_mapping.get(packageid=pkg_dict['id'])

            if visibilityRecord is None:
                newVisibility = db.granular_visibility_mapping()
                newVisibility.visibilityid = pkg_dict['visibilityid']
                newVisibility.packageid = pkg_dict['id']
                newVisibility.save()

                session = context['session']
                session.add(newVisibility)
                session.commit()

            else:
                session = context['session']
                visibilityRecord.visibilityid = pkg_dict['visibilityid'] 
                visibilityRecord.save()
                session.commit()
            
            data = {"visibilityid": pkg_dict['visibilityid']}
            ispublic = toolkit.get_action('get_visibility')({'ignore_auth': True}, data)

            #Get then update package with new mapping for private from the visibility
            data = {"id": pkg_dict['id']}
            Complete_pkg_dict = toolkit.get_action('package_show')({'ignore_auth': True}, data)

            Complete_pkg_dict["private"] = ispublic.ckanmapping
            test = toolkit.get_action('package_update')({'ignore_auth': True}, Complete_pkg_dict)

    # ITemplateHelpers
    def get_helpers(self):
        return {'get_visibilities': helpers.get_visibilities,
                "is_selected": helpers.is_selected}

    # IAuthFunctions
    def get_auth_functions(self):
        auth_dict = {
            'isAdmin': auth.isAdmin
        }
        return auth_dict

    # IActions
    def get_actions(self):
        actions_dict = {
            "get_package_visibility": actionsapi.get_package_visibility,
            'get_visibility_mapping': actionsapi.get_visibility_mapping,
            'add_visibility': actionsapi.add_visibility,
            "get_visibility": actionsapi.get_visibility,
        }
        return actions_dict

    # IBlueprint
    def get_blueprint(self):
        u'''Return a Flask Blueprint object to be registered by the app.'''

        # Create Blueprint for plugin
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = u'templates'
        # Add plugin url rules to Blueprint object
        rules = [
            (u'/ckan-admin/visibility', u'admin/visibility', visibility_show),
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint


    

