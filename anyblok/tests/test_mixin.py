from anyblok.tests.testcase import TestCase
from anyblok.registry import RegistryManager
from anyblok import Declarations
target_registry = Declarations.target_registry
remove_registry = Declarations.remove_registry
Mixin = Declarations.Mixin


class OneInterface:
    pass


class TestCoreInterfaceMixin(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestCoreInterfaceMixin, cls).setUpClass()
        RegistryManager.init_blok('testMixin')
        Declarations.current_blok = 'testMixin'

    @classmethod
    def tearDownClass(cls):
        super(TestCoreInterfaceMixin, cls).tearDownClass()
        Declarations.current_blok = None
        del RegistryManager.loaded_bloks['testMixin']

    def setUp(self):
        super(TestCoreInterfaceMixin, self).setUp()
        blokname = 'testMixin'
        RegistryManager.loaded_bloks[blokname]['Mixin'] = {
            'registry_names': []}

    def assertInMixin(self, *args):
        blokname = 'testMixin'
        blok = RegistryManager.loaded_bloks[blokname]
        self.assertEqual(len(blok['Mixin']['Mixin.MyMixin']['bases']),
                         len(args))
        for cls_ in args:
            has = cls_ in blok['Mixin']['Mixin.MyMixin']['bases']
            self.assertEqual(has, True)

    def test_add_interface(self):
        target_registry(Mixin, cls_=OneInterface, name_='MyMixin')
        self.assertEqual('Mixin', Mixin.MyMixin.__declaration_type__)
        self.assertInMixin(OneInterface)
        dir(Declarations.Mixin.MyMixin)

    def test_add_interface_with_decorator(self):

        @target_registry(Mixin)
        class MyMixin:
            pass

        self.assertEqual('Mixin', Mixin.MyMixin.__declaration_type__)
        self.assertInMixin(MyMixin)

    def test_add_two_interface(self):

        target_registry(Mixin, cls_=OneInterface, name_="MyMixin")

        @target_registry(Mixin)
        class MyMixin:
            pass

        self.assertInMixin(OneInterface, MyMixin)

    def test_remove_interface_with_1_cls_in_registry(self):

        target_registry(Mixin, cls_=OneInterface, name_="MyMixin")
        self.assertInMixin(OneInterface)
        blokname = 'testMixin'
        remove_registry(Mixin, cls_=OneInterface, name_="MyMixin",
                        blok=blokname)

        blokname = 'testMixin'
        self.assertEqual(hasattr(Mixin, blokname), False)
        self.assertInMixin()

    def test_remove_interface_with_2_cls_in_registry(self):

        target_registry(Mixin, cls_=OneInterface, name_="MyMixin")

        @target_registry(Mixin)
        class MyMixin:
            pass

        self.assertInMixin(OneInterface, MyMixin)
        blokname = 'testMixin'
        remove_registry(Mixin, cls_=OneInterface, name_="MyMixin",
                        blok=blokname)
        self.assertInMixin(MyMixin)
