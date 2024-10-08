# Generated by Django 4.2.15 on 2024-09-27 19:38

from django.db import migrations

"""
Update the created_by field on Advisory from the old qualified_name
to the new pipeline_id.
"""


def update_created_by(apps, schema_editor):
    from vulnerabilities.pipelines.nvd_importer import NVDImporterPipeline

    Advisory = apps.get_model("vulnerabilities", "Advisory")
    Advisory.objects.filter(created_by="vulnerabilities.importers.nvd.NVDImporter").update(
        created_by=NVDImporterPipeline.pipeline_id
    )



def reverse_update_created_by(apps, schema_editor):
    from vulnerabilities.pipelines.nvd_importer import NVDImporterPipeline

    Advisory = apps.get_model("vulnerabilities", "Advisory")
    Advisory.objects.filter(created_by=NVDImporterPipeline.pipeline_id).update(
        created_by="vulnerabilities.importers.nvd.NVDImporter"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("vulnerabilities", "0067_update_github_advisory_created_by"),
    ]

    operations = [
        migrations.RunPython(update_created_by, reverse_code=reverse_update_created_by),
    ]
