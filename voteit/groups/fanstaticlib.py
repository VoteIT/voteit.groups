""" Fanstatic lib"""
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource

from voteit.core.fanstaticlib import voteit_main_css
from voteit.core.fanstaticlib import base_js


groups_lib = Library('groups_static', 'static')


group_proposals_js = Resource(groups_lib, 'group_proposals.js', depends = (base_js,))
group_proposals_css = Resource(groups_lib, 'group_proposals.css', depends = (voteit_main_css,))
group_proposals = Group((group_proposals_js, group_proposals_css))
