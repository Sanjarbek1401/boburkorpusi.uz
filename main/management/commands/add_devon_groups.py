from django.core.management.base import BaseCommand
from main.models import DevonGroup, DevonCategory


class Command(BaseCommand):
    help = "1 dan 99 gacha bo'lgan DevonGroup'larni Fard kategoriyasiga qo'shadi"

    def handle(self, *args, **kwargs):
        try:
            category = DevonCategory.objects.get(name="Fard")  # "Fard" nomli kategoriya borligini tekshiramiz
        except DevonCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR('Kategoriya "Fard" topilmadi.'))
            return

        groups_to_create = [
            DevonGroup(category=category, name=str(i), order=i)
            for i in range(1, 100)
        ]

        DevonGroup.objects.bulk_create(groups_to_create)
        self.stdout.write(self.style.SUCCESS("1 dan 99 gacha bo'lgan Devon guruhlari muvaffaqiyatli qo'shildi!"))
