from django.test import TestCase
from findings.models import Finding, Scan
from django.db.utils import IntegrityError


class TestFindingModel(TestCase):
    def setUp(self) -> None:
        self.finding_obj = {
            "target_id": "abcd",
            "definition_id": "efgh",
            "url": "http://gam.com",
            "path": "http://gam.com",
            "method": "get",
        }

        self.finding_model_fields_max_lengths = {
            "target_id": 50,
            "definition_id": 50,
            "url": 200,
            "path": 200,
            "method": 7,
        }

    def test_model_field_max_length(self):
        for field, max_length in self.finding_model_fields_max_lengths.items():
            self.assertEquals(Finding._meta.get_field(field).max_length, max_length)

    def test_create_finding_object(self):
        obj = Finding.objects.create(**self.finding_obj)
        self.assertEqual(Finding.objects.count(), 1)
        self.assertEqual(Finding.objects.get(id=obj.id), obj)
        for key, value in self.finding_obj.items():
            self.assertEqual(getattr(obj, key), value)

    def test_invalid_method_field_raises_error(self):
        bad_obj = self.finding_obj
        bad_obj["method"] = "bad_method"
        with self.assertRaises(IntegrityError):
            Finding.objects.create(**bad_obj)

    def test_finding_model_ordered_by_id(self):
        for i in range(3):
            Finding.objects.create(**self.finding_obj)
        expected_id_order = [1, 2, 3]
        id_order = Finding.objects.values_list("id", flat=True)
        self.assertEqual(expected_id_order, list(id_order))


class TestScanModel(TestCase):
    def setUp(self) -> None:
        finding_dict = {
            "target_id": "abcd",
            "definition_id": "efgh",
            "url": "http://gam.com",
            "path": "http://gam.com",
            "method": "get",
        }
        self.finding_obj = Finding.objects.create(**finding_dict)
        self.scans = [
            "226RQgVAVaA7",
            "24hiHkcNwqCs",
            "24kdTiUTi9qu",
        ]

        self.scan_model_fields_max_lengths = {
            "scan": 50,
        }

    def test_model_field_max_length(self):
        for field, max_length in self.scan_model_fields_max_lengths.items():
            self.assertEquals(Scan._meta.get_field(field).max_length, max_length)

    def test_create_scan_object(self):
        for scan in self.scans:
            Scan.objects.create(finding=self.finding_obj, scan=scan)
        self.assertEqual(Scan.objects.count(), len(self.scans))
        self.assertEqual(Scan.objects.order_by('id').first().scan, self.scans[0])
        self.assertEqual(Scan.objects.order_by('id').first().finding, self.finding_obj)

