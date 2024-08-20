#
# Copyright (c) nexB Inc. and others. All rights reserved.
# VulnerableCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/aboutcode-org/vulnerablecode for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

from unittest.mock import patch

from django.test import TestCase

from vulnerabilities import models
from vulnerabilities.pipelines import VulnerableCodeBaseImporterPipeline
from vulnerabilities.tests import advisory1
from vulnerabilities.tests import advisory_data1


class TestVulnerableCodeBaseImporterPipeline(TestCase):
    @patch.object(
        VulnerableCodeBaseImporterPipeline,
        "collect_advisories",
        return_value=[advisory_data1],
    )
    @patch.object(
        VulnerableCodeBaseImporterPipeline,
        "advisories_count",
        return_value=1,
    )
    def test_collect_and_store_advisories(self, mock_advisories_count, mock_collect_advisories):
        self.assertEqual(0, models.Advisory.objects.count())

        base_pipeline = VulnerableCodeBaseImporterPipeline()
        base_pipeline.collect_and_store_advisories()

        mock_advisories_count.assert_called_once()
        mock_collect_advisories.assert_called_once()

        self.assertEqual(1, models.Advisory.objects.count())

        collected_advisory = models.Advisory.objects.first()
        result_aliases = collected_advisory.aliases
        expected_aliases = advisory_data1.aliases

        self.assertEqual(expected_aliases, result_aliases)
        self.assertEqual(base_pipeline.qualified_name, collected_advisory.created_by)

    def test_import_new_advisories(self):
        self.assertEqual(0, models.Vulnerability.objects.count())

        base_pipeline = VulnerableCodeBaseImporterPipeline()
        base_pipeline.new_advisories = [advisory1]
        base_pipeline.import_new_advisories()

        self.assertEqual(1, models.Vulnerability.objects.count())

        imported_vulnerability = models.Vulnerability.objects.first()

        self.assertEqual(1, imported_vulnerability.aliases.count())

        expected_alias = imported_vulnerability.aliases.first()
        self.assertEqual(advisory1.aliases[0], expected_alias.alias)
