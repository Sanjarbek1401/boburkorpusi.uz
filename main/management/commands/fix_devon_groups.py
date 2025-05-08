from django.core.management.base import BaseCommand
from main.models import DevonGroup, DevonCategory


class Command(BaseCommand):
    help = "Devon guruhlarini tartibga solish va yetishmayotgan raqamlarni qo'shish"

    def handle(self, *args, **kwargs):
        try:
            category = DevonCategory.objects.get(name="Masnaviy")
        except DevonCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR('Kategoriya "Masnaviy" topilmadi.'))
            return

        # Mavjud guruhlarni o'chirish
        DevonGroup.objects.filter(category=category).delete()

        # 1 dan 99 gacha yangi guruhlarni yaratish
        groups_to_create = [
            DevonGroup(category=category, name=str(i), order=i)
            for i in range(1, 355)
        ]

        DevonGroup.objects.bulk_create(groups_to_create)
        self.stdout.write(self.style.SUCCESS("Devon guruhlari muvaffaqiyatli tartibga solindi!"))
