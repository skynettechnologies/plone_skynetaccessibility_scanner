"""
scanner.py — Plone browser views for SkynetAccessibility Scanner.

Views registered:
  @@skynet-scanner        — Main dashboard (control panel page)
  @@skynet-user-info      — JSON endpoint: current Plone user info
  @@skynet-save-settings  — JSON endpoint: save settings from JS
"""
import json

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from plone.skynetaccessibility_Scanner.interfaces import ISkynetScannerSettings


def _get_cfg():
    """Load settings from Plone registry. Returns proxy or None."""
    try:
        registry = getUtility(IRegistry)
        return registry.forInterface(ISkynetScannerSettings, check=False)
    except Exception:
        return None


class ScannerDashboardView(BrowserView):
    """Renders the SkynetAccessibility Scanner dashboard inside Plone."""

    def __call__(self):
        return self.index()

    def website_domain(self):
        cfg = _get_cfg()
        if cfg and cfg.website_domain:
            return cfg.website_domain
        req = self.request
        server_url = req.get('SERVER_URL', '')
        if server_url:
            return server_url
        host = req.get('HTTP_HOST', 'localhost')
        scheme = 'https' if req.get('HTTPS') == 'on' else 'http'
        return '{}://{}'.format(scheme, host.split(':')[0])

    def website_id(self):
        cfg = _get_cfg()
        return cfg.website_id if cfg else ''

    def dashboard_link(self):
        cfg = _get_cfg()
        return cfg.dashboard_link if cfg else ''

    def settings_json(self):
        cfg = _get_cfg()
        if not cfg:
            return '{}'
        data = {
            'website_domain':        cfg.website_domain       or '',
            'website_id':            cfg.website_id           or '',
            'dashboard_link':        cfg.dashboard_link       or '',
            'fav_icon':              cfg.fav_icon             or '',
            'plan_state':            cfg.plan_state           or 'free',
            'package_name':          cfg.package_name         or '',
            'package_id_ext':        cfg.package_id_ext       or '',
            'page_views':            cfg.page_views           or '',
            'subscr_interval':       cfg.subscr_interval      or '',
            'end_date':              cfg.end_date             or '',
            'cancel_date':           cfg.cancel_date          or '',
            'paypal_subscr_id':      cfg.paypal_subscr_id     or '',
            'package_price':         cfg.package_price        or '',
            'final_price':           cfg.final_price          or 0.0,
            'is_trial_period':       bool(cfg.is_trial_period),
            'is_expired':            bool(cfg.is_expired),
            'is_cancelled':          bool(cfg.is_cancelled),
            'scan_status':           cfg.scan_status          or 0,
            'url_scan_status':       cfg.url_scan_status      or 0,
            'total_pages':           cfg.total_pages          or 0,
            'total_scan_pages':      cfg.total_scan_pages     or 0,
            'total_selected_pages':  cfg.total_selected_pages or 0,
            'total_last_scan_pages': cfg.total_last_scan_pages or 0,
            'last_url_scan':         cfg.last_url_scan        or '',
            'last_scan':             cfg.last_scan            or '',
            'next_scan_date':        cfg.next_scan_date       or '',
            'success_percentage':    cfg.success_percentage   or 0.0,
            'total_violations':      cfg.total_violations     or 0,
            'total_fail':            cfg.total_fail           or 0,
            'total_success':         cfg.total_success        or 0,
            'plans_json':            cfg.plans_json           or '',
            'error_message':         cfg.error_message        or '',
        }
        return json.dumps(data)

    def static_prefix(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        return '{}/++resource++plone.skynetaccessibility_Scanner'.format(portal_url)

    def user_info_url(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        return '{}/@@skynet-user-info'.format(portal_url)

    def save_settings_url(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        return '{}/@@skynet-save-settings'.format(portal_url)

    def proxy_url(self):
        """Base portal URL passed to JS as data-portal-url so proxyUrl() works correctly."""
        portal_url = getToolByName(self.context, 'portal_url')()
        return portal_url


class UserInfoView(BrowserView):
    """Returns the currently logged-in Plone user's info as JSON."""

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.isAnonymousUser():
            self.request.response.setStatus(401)
            return json.dumps({'is_authenticated': False})
        member = mtool.getAuthenticatedMember()
        user_id = member.getId()
        email    = member.getProperty('email',    '') or ''
        fullname = member.getProperty('fullname', '') or ''
        name     = fullname or user_id
        return json.dumps({
            'is_authenticated': True,
            'uid':              user_id,
            'username':         user_id,
            'email':            email,
            'name':             name,
        })


class SaveSettingsView(BrowserView):
    """Saves settings POSTed from the JS dashboard back to plone.app.registry."""

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        try:
            registry = getUtility(IRegistry)
            cfg = registry.forInterface(ISkynetScannerSettings, check=False)
        except Exception as e:
            self.request.response.setStatus(500)
            return json.dumps({'status': 'error', 'message': str(e)})

        form = self.request.form

        text_fields = [
            'website_domain', 'website_id', 'dashboard_link', 'fav_icon',
            'plan_state', 'package_name', 'package_id_ext', 'page_views',
            'subscr_interval', 'end_date', 'cancel_date', 'paypal_subscr_id',
            'package_price', 'last_url_scan', 'last_scan', 'next_scan_date',
            'plans_json', 'active_view', 'error_message',
        ]
        for field in text_fields:
            if field in form:
                setattr(cfg, field, form[field] or u'')

        int_fields = [
            'scan_status', 'url_scan_status', 'total_pages', 'total_scan_pages',
            'total_selected_pages', 'total_last_scan_pages',
            'total_violations', 'total_fail', 'total_success',
        ]
        for field in int_fields:
            if field in form:
                try:
                    setattr(cfg, field, int(form[field]))
                except (ValueError, TypeError):
                    pass

        float_fields = ['final_price', 'success_percentage']
        for field in float_fields:
            if field in form:
                try:
                    setattr(cfg, field, float(form[field]))
                except (ValueError, TypeError):
                    pass

        bool_fields = ['is_trial_period', 'is_expired', 'is_cancelled']
        for field in bool_fields:
            if field in form:
                val = form[field]
                setattr(cfg, field, val in ('true', 'True', '1', True))

        return json.dumps({'status': 'ok'})
