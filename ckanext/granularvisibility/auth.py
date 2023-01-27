import ckan.authz as authz

#Auth check
#Checks if user is a sysadmin
def _user_has_minumum_role(context):

    user = context['user']

    # Always let sysadmins do their thing.
    if user["sysadmin"]:
        return {'success': True}
    else:
        return {'success': False}

def isAdmin(context):
    return _user_has_minumum_role(context)