from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from findings.serializers import FindingSerializer
from findings.views import FindingsPaginator
from findings.models import Finding
import math


class FindingListViewTest(APITestCase):
    fixtures = ["finding.json", "scan.json"]

    def setUp(self) -> None:
        self.expected_page_size = FindingsPaginator.page_size

    def test_api_response(self):
        expected_response_keys = [
            "count",
            "page_total",
            "page",
            "length",
            "previous",
            "next",
            "results",
        ]

        expected_total_pages = math.ceil(
            Finding.objects.count() / self.expected_page_size
        )
        response = self.client.get(reverse("findings_list"))
        response_keys = list(response.data.keys())
        for key in expected_response_keys:
            self.assertIn(key, response_keys)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["length"], self.expected_page_size)
        self.assertEqual(response.data["count"], Finding.objects.count())
        self.assertEqual(response.data["page_total"], int(expected_total_pages))

        queryset = Finding.objects.prefetch_related("scans").all()[
            : self.expected_page_size
        ]
        self.assertEqual(
            response.data["results"], FindingSerializer(queryset, many=True).data
        )

    def test_filtered_api_response(self):
        definition_id = "0fR9GA5lgbo6"
        scan = "226RQgVAVaA7"
        url = reverse("findings_list")

        definition_response = self.client.get(f"{url}?definition_id={definition_id}")
        scan_response = self.client.get(f"{url}?scan={scan}")

        definition_queryset = Finding.objects.filter(definition_id=definition_id)
        scan_queryset = Finding.objects.filter(scans__scan=scan)

        definition_queryset_size = definition_queryset.count()
        scan_queryset_size = scan_queryset.count()

        self.assertEqual(definition_response.data["count"], definition_queryset_size)
        self.assertEqual(scan_response.data["count"], scan_queryset_size)

        self.assertEqual(
            definition_response.data["results"],
            FindingSerializer(
                definition_queryset[: self.expected_page_size], many=True
            ).data,
        )
        self.assertEqual(
            scan_response.data["results"],
            FindingSerializer(scan_queryset[: self.expected_page_size], many=True).data,
        )
