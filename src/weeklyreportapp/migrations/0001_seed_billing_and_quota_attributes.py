from django.db import migrations


def forwards(apps, schema_editor):
    # ColdFront models (via historical app registry)
    AttributeType = apps.get_model("resources", "AttributeType")
    AllocationAttributeType = apps.get_model("allocations", "AllocationAttributeType")
    ResourceAttributeType = apps.get_model("resources", "ResourceAttributeType")

    # AttributeType names are defined by ColdFront; commonly: "Int", "Float", "Text", "Yes/No"
    int_type = AttributeType.objects.get(name="Int")
    float_type = AttributeType.objects.get(name="Float")

    # 1) AllocationAttributeType: "Quota in Bytes"
    # Pick values that fit your policy; these are safe defaults for a quota attribute.
    AllocationAttributeType.objects.get_or_create(
        name="Quota in Bytes",
        defaults={
            "attribute_type": int_type,
            "has_usage": False,
            "is_required": False,
            "is_unique": False,
            "is_private": False,
            "is_changeable": True,  # nice if you want PIs/managers to request quota changes
        },
    )

    # 2) ResourceAttributeType: "cost_per_terabyte"
    ResourceAttributeType.objects.get_or_create(
        name="cost_per_terabyte",
        defaults={
            "attribute_type": float_type,
            "is_required": False,
            "is_value_unique": False,
        },
    )

    # NOTE: "requires_payment" is a boolean field on Resource (not an attribute type),
    # so there is nothing to create here. You’ll set it per Resource in admin or via code.


def backwards(apps, schema_editor):
    # Conservative reverse: only delete the types if they exist.
    # (If you already have allocations/resources using them, you may NOT want to delete.)
    AllocationAttributeType = apps.get_model("allocations", "AllocationAttributeType")
    ResourceAttributeType = apps.get_model("resources", "ResourceAttributeType")

    AllocationAttributeType.objects.filter(name="Quota in Bytes").delete()
    ResourceAttributeType.objects.filter(name="cost_per_terabyte").delete()


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
