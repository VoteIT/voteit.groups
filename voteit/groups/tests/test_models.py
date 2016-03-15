import unittest

from pyramid import testing
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from voteit.groups.interfaces import IGroup
from voteit.groups.interfaces import IGroups
from voteit.groups.interfaces import IGroupRecommendations


class GroupTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.groups.models import Group
        return Group

    def test_verify_class(self):
        self.assertTrue(verifyClass(IGroup, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IGroup, self._cut()))

    def test_set_members(self):
        userids = ['a', 'b', 'c']
        obj = self._cut()
        obj.members = userids
        self.assertEqual(obj.get_field_value('members'), frozenset(userids)) #b/c compat test
        self.assertEqual(obj.members, frozenset(userids))


class GroupsTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.groups.models import Groups
        return Groups

    def test_verify_class(self):
        self.assertTrue(verifyClass(IGroups, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IGroups, self._cut()))


class GroupRecommendationTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.groups.models import GroupRecommendations
        return GroupRecommendations

    @property
    def _proposal(self):
        from voteit.core.models.proposal import Proposal
        return Proposal

    def test_verify_class(self):
        self.assertTrue(verifyClass(IGroupRecommendations, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IGroupRecommendations, self._cut(self._proposal())))

    def test_get_group_data_nonexistent_group(self):
        obj = self._cut(self._proposal())
        null = object()
        self.assertEqual(obj.get('the_404s', null), null)

    def test_get_group_data(self):
        obj = self._cut(self._proposal())
        obj['200s'] =  dict(we='are', found=1)
        null = object()
        result = obj.get('200s', null)
        self.assertEqual(dict(result), {'we': 'are', 'found': 1})

    def test_get_other_group_data(self):
        obj = self._cut(self._proposal())
        obj['200s'] = dict(we='are', found=1)
        obj['202s'] = dict(are='they', real=1)
        self.assertEqual(dict(obj.get('200s')), {'we': 'are', 'found': 1})
        self.assertEqual(dict(obj.get('202s')), {'are': 'they', 'real': 1})

    def test_count_states(self):
        obj = self._cut(self._proposal())
        obj['200s'] = {'state': 'one'}
        obj['201s'] = {'state': 'one'}
        obj['202s'] = {'state': 'one'}
        obj['203s'] = {}
        obj['204s'] = {'state': 'two'}
        self.assertEqual(obj.count_states(),
                         {'one': 3, '': 1, 'two': 1})

    def test_integration(self):
        self.config.include('arche.testing')
        self.config.include('arche.testing.portlets')
        self.config.include('voteit.groups')
        prop = self._proposal()
        adapter = self.config.registry.queryAdapter(prop, IGroupRecommendations)
        self.failUnless(adapter)
