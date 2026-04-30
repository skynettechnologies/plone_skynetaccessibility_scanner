# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope import schema


class IPloneSkynetLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ISkynetScannerSettings(Interface):
    """Persistent settings for SkynetAccessibility Scanner."""

    website_domain        = schema.TextLine(title=u"Website Domain",           required=False, default=u"")
    website_id            = schema.TextLine(title=u"Website ID",               required=False, default=u"")
    dashboard_link        = schema.TextLine(title=u"Dashboard Link",           required=False, default=u"")
    fav_icon              = schema.TextLine(title=u"Favicon URL",              required=False, default=u"")
    plan_state            = schema.TextLine(title=u"Plan State",               required=False, default=u"free")
    package_name          = schema.TextLine(title=u"Package Name",             required=False, default=u"")
    package_id_ext        = schema.TextLine(title=u"Package ID Ext",           required=False, default=u"")
    page_views            = schema.TextLine(title=u"Page Views",               required=False, default=u"")
    subscr_interval       = schema.TextLine(title=u"Billing Interval",         required=False, default=u"")
    end_date              = schema.TextLine(title=u"Plan End Date",            required=False, default=u"")
    cancel_date           = schema.TextLine(title=u"Cancel Date",              required=False, default=u"")
    paypal_subscr_id      = schema.TextLine(title=u"PayPal Subscription ID",   required=False, default=u"")
    package_price         = schema.TextLine(title=u"Package Price",            required=False, default=u"")
    final_price           = schema.Float(   title=u"Final Price",              required=False, default=0.0)
    is_trial_period       = schema.Bool(    title=u"Is Trial Period",          required=False, default=False)
    is_expired            = schema.Bool(    title=u"Is Expired",               required=False, default=False)
    is_cancelled          = schema.Bool(    title=u"Is Cancelled",             required=False, default=False)
    scan_status           = schema.Int(     title=u"Scan Status",              required=False, default=0)
    url_scan_status       = schema.Int(     title=u"URL Scan Status",          required=False, default=0)
    total_pages           = schema.Int(     title=u"Total Pages",              required=False, default=0)
    total_scan_pages      = schema.Int(     title=u"Total Scanned Pages",      required=False, default=0)
    total_selected_pages  = schema.Int(     title=u"Total Selected Pages",     required=False, default=0)
    total_last_scan_pages = schema.Int(     title=u"Total Last Scan Pages",    required=False, default=0)
    last_url_scan         = schema.TextLine(title=u"Last URL Scan",            required=False, default=u"")
    last_scan             = schema.TextLine(title=u"Last Scan",                required=False, default=u"")
    next_scan_date        = schema.TextLine(title=u"Next Scan Date",           required=False, default=u"")
    success_percentage    = schema.Float(   title=u"Success Percentage",       required=False, default=0.0)
    total_violations      = schema.Int(     title=u"Total Violations",         required=False, default=0)
    total_fail            = schema.Int(     title=u"Failed Checks",            required=False, default=0)
    total_success         = schema.Int(     title=u"Passed Checks",            required=False, default=0)
    plans_json            = schema.Text(    title=u"Plans JSON",               required=False, default=u"")
    active_view           = schema.TextLine(title=u"Active View",              required=False, default=u"main")
    error_message         = schema.TextLine(title=u"Error Message",            required=False, default=u"")
