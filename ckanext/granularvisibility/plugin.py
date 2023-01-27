import ckan.model as model
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.granularvisibility.converters_validators as converters_validators
import ckanext.granularvisibility.actionsapi as actionsapi
import ckanext.granularvisibility.helpers as helpers
import ckanext.granularvisibility.auth as auth
import ckanext.granularvisibility.db as db

class GranularvisibilityPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)

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
        schema.update({
                'visibilityid': [
                    toolkit.get_validator('ignore_missing'),
                    converters_validators.set_ckan_visiability
                ]
            })
        return schema

    def update_package_schema(self):
        schema = super(GranularvisibilityPlugin, self).update_package_schema()
        schema.update({
                'visibilityid': [
                    toolkit.get_validator('ignore_missing'),
                    converters_validators.set_ckan_visiability
                ]
            })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

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


    

