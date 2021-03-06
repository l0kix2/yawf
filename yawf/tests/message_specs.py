from django.test import TestCase

from yawf.messages.spec import MessageSpec
from yawf.messages.common import message_spec_fabric

__all__ = ('MessageSpecsTestCase',)


class MessageSpecsTestCase(TestCase):

    def test_grouping(self):

        class Spec1(MessageSpec):
            id = 'edit'

        self.assertFalse(Spec1().is_grouped)

        class SpecWithGrouping(MessageSpec):
            id = 'edit__personality__name'
        self.assertTrue(SpecWithGrouping().is_grouped)

    def test_without_id(self):

        class WrongSpec(MessageSpec):
            verb = 'push me!'

        self.assertRaises(ValueError, WrongSpec)

    def test_validator(self):

        class CustomValidator:
            __init__ = lambda self, data: None
            is_valid = lambda self: True
            cleaned_data = {'buz': 'fuz'}

        class Spec(MessageSpec):

            id = 'test'
            validator_cls = CustomValidator

        v = Spec().validator_cls({})
        self.assertTrue(v.is_valid())
        self.assertItemsEqual(
            v.cleaned_data,
            {'buz': 'fuz'})

        class Spec2(Spec):

            class Validator:
                __init__ = lambda self, data: None
                is_valid = lambda self: True
                cleaned_data = {'foo': 'bar'}

        v = Spec2().validator_cls({})
        self.assertTrue(v.is_valid())
        self.assertItemsEqual(
            v.cleaned_data,
            {'foo': 'bar'})

    def test_repr(self):

        class SpecWithoutVerb(MessageSpec):

            id = 'foo'

        self.assertEqual(unicode(SpecWithoutVerb()), 'foo')

        class SpecWithVerb(SpecWithoutVerb):

            verb = 'foobar'

        self.assertEqual(unicode(SpecWithVerb()), 'foobar')

    def test_fabric(self):

        spec = message_spec_fabric(id='cancel')
        self.assertEqual(spec.id, 'cancel')
        self.assertTrue(isinstance(spec, MessageSpec))
