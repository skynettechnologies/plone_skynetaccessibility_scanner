# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "plone.skynetaccessibility_Scanner:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["plone.skynetaccessibility_Scanner.upgrades"]


def post_install(context):
    """Post install script — runs after addon is installed."""
    pass


def uninstall(context):
    """Uninstall script — runs after addon is uninstalled."""
    pass
