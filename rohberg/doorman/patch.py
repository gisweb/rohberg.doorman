from Products.CMFPlone.RegistrationTool import RegistrationTool
from Products.CMFCore.utils import _checkPermission
from Products.CMFDefault.permissions import ManagePortal
from Products.CMFDefault.utils import checkEmailAddress
from Products.PluggableAuthService.interfaces.plugins import \
    IValidationPlugin, IPropertiesPlugin

from rohberg.doorman import RDMessageFactory as _

# TODO: patch: Not nice. Can we do better? 

def testPasswordValidity(self, password, confirm=None):

    """ Verify that the password satisfies the portal's requirements.

    o If the password is valid, return None.
    o If not, return a string explaining why.
    """
    if not password:
        return _(u'You must enter a password.')

    # if len(password) < 5 and not _checkPermission(ManagePortal, self):
    #     return _(u'Your password must contain at least 5 characters.')

    if confirm is not None and confirm != password:
        return _(u'Your password and confirmation did not match. '
                 u'Please try again.')

    # return None
    
    # changes:
    # Use PAS to test validity
    pas_instance = self.acl_users
    plugins = pas_instance._getOb('plugins')
    validators = plugins.listPlugins(IValidationPlugin)
    err = []
    for validator_id, validator in validators:
        user = None
        set_id = ''
        set_info = {'password':password}
        errors = validator.validateUserInfo( user, set_id, set_info )
        err += [info['error'] for info in errors if info['id'] == 'password' ]
    if err:
        return ' '.join(err)
    else:
        # original policy if no custom policy defined
        if len(password) < 5 and not _checkPermission(ManagePortal, self):
            return _(u'Your password must contain at least 5 characters.')
        return None
    
    
def patchTestPasswordValidity():
    RegistrationTool.original_testPasswordValidity = RegistrationTool.testPasswordValidity
    RegistrationTool.testPasswordValidity = testPasswordValidity


import random, string, itertools
myrg = random.SystemRandom()

alphabets = [string.lowercase, string.uppercase, string.digits, string.punctuation]
alphabet = "+".join(alphabets)

def getPassword(length=8, s=None):
    length = length>=20 and langth or 20
    password = []
    for group in alphabets:
        password += random.sample(group, 2)
    password += (length>len(password)) and random.sample(alphabet, (length - len(password))) or ""
    random.shuffle(password)
    return ''.join(password)
    
def patchGetPassword():
    RegistrationTool.original_getPassword = RegistrationTool.getPassword
    RegistrationTool.getPassword = getPassword