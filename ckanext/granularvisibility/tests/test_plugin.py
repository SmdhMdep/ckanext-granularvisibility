import ckanext.granularvisibility.plugin as plugin
import ckan.tests.factories as factories
import ckan.plugins.toolkit as toolkit

from ckan import model

import pytest

############################
##########  Auth  ##########
############################

@pytest.mark.ckan_config('ckan.plugins','granularvisibility')
@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
def test_Auth():
    #Create an admin and a normal user
    admin = factories.Sysadmin()
    user = factories.User()

    #normal user should be able to get auth
    context = {'model': model, 'session': model.Session, 'user': user}
    assert plugin.auth._user_has_minumum_role(context) == {'success': False}

    #admin should be authed
    context = {'model': model, 'session': model.Session, 'user': admin}
    assert plugin.auth._user_has_minumum_role(context) == {'success': True}
    
###########################
##########  API  ##########
###########################

@pytest.mark.ckan_config('ckan.plugins','granularvisibility')
@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
def test_api_add_visibility(): #Done first to test ready for use in TestApi Class
    data = {'visibility': "Test",'ckanmapping': False, 'description': "This is a test"}
    visibility = toolkit.get_action('add_visibility')({'ignore_auth': True}, data)

    assert visibility is not None

@pytest.mark.ckan_config('ckan.plugins','granularvisibility')
@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
class TestApi():
    def setup(self):
        # Create a dataset that will be used for testing
        admin = factories.User()
        owner_org = factories.Organization(admin=[{
            'name': admin['id'],
            'capacity': 'admin'
        }])
        self.dataset = factories.Dataset(owner_org=owner_org['id'])

        #Add a new testing visibility
        data = {'visibility': "Test",'ckanmapping': False, 'description': "This is a test"}
        self.visibility = toolkit.get_action('add_visibility')({'ignore_auth': True}, data)

        #Create a mapping between the new dataset and visibility
        newMapping = plugin.db.granular_visibility_mapping()

        newMapping.packageid = self.dataset['id']
        newMapping.visibilityid = self.visibility.visibilityid
        newMapping.save()

        context = {'model': model, 'session': model.Session, 'ignore_auth': True}
        session = context['session']
        session.add(newMapping)
        session.commit()

    def test_api_get_package_visibility(self):
        data = {'packageid': str(self.dataset['id'])}
        newVisibility = toolkit.get_action('get_package_visibility')({'ignore_auth': True}, data)

        assert newVisibility.visibilityid == self.visibility.visibilityid

    def test_api_get_visibility_mapping(self):
        data = {'visibilityid': str(self.visibility.visibilityid)}
        mapping = toolkit.get_action('get_visibility_mapping')({'ignore_auth': True}, data)

        assert mapping == False

    def test_api_get_visibility(self):
        data = {'visibilityid': str(self.visibility.visibilityid)}
        visibilityInfo = toolkit.get_action('get_visibility')({'ignore_auth': True}, data)

        assert visibilityInfo.visibilityid == self.visibility.visibilityid
        assert visibilityInfo.visibility == self.visibility.visibility
        assert visibilityInfo.ckanmapping == self.visibility.ckanmapping
        assert visibilityInfo.description == self.visibility.description

###############################
##########  Helpers  ##########
###############################

@pytest.mark.ckan_config('ckan.plugins','granularvisibility')
@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
def test_helper_get_visibilities():
    #Add a new testing visibility
    data = {'visibility': "Test",'ckanmapping': False, 'description': "This is a test"}
    vis1 = toolkit.get_action('add_visibility')({'ignore_auth': True}, data)

    #Add a new testing visibility
    data = {'visibility': "Test2",'ckanmapping': True, 'description': "This is a second test"}
    vis2 = toolkit.get_action('add_visibility')({'ignore_auth': True}, data)

    visibilitylist = plugin.helpers.get_visibilities()

    #Test that vis1 is correctly returned
    assert visibilitylist[0].visibilityid == vis1.visibilityid
    assert visibilitylist[0].visibility == vis1.visibility
    assert visibilitylist[0].ckanmapping == vis1.ckanmapping
    assert visibilitylist[0].description == vis1.description

    #Test that vis2 is correctly returned
    assert visibilitylist[1].visibilityid == vis2.visibilityid
    assert visibilitylist[1].visibility == vis2.visibility
    assert visibilitylist[1].ckanmapping == vis2.ckanmapping
    assert visibilitylist[1].description == vis2.description

@pytest.mark.ckan_config('ckan.plugins','granularvisibility')
@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
def test_helper_is_selected():

    # Create a dataset that will be used for testing
    admin = factories.User()
    owner_org = factories.Organization(admin=[{
        'name': admin['id'],
        'capacity': 'admin'
    }])
    dataset = factories.Dataset(owner_org=owner_org['id'])

    #Add a new testing visibility
    data = {'visibility': "Test",'ckanmapping': False, 'description': "This is a test"}
    visibilityTrue = toolkit.get_action('add_visibility')({'ignore_auth': True}, data)

    data = {'visibility': "Test2",'ckanmapping': True, 'description': "This is a test 2"}
    visibilityFalse = toolkit.get_action('add_visibility')({'ignore_auth': True}, data)

    #Create a mapping between the new dataset and visibility
    newMapping = plugin.db.granular_visibility_mapping()

    newMapping.packageid = dataset['id']
    newMapping.visibilityid = visibilityTrue.visibilityid
    newMapping.save()

    context = {'model': model, 'session': model.Session, 'ignore_auth': True}
    session = context['session']
    session.add(newMapping)
    session.commit()

    #test a true and false case
    assert plugin.helpers.is_selected(dataset['id'], visibilityTrue.visibilityid) == True
    assert plugin.helpers.is_selected(dataset['id'], visibilityFalse.visibilityid) == False