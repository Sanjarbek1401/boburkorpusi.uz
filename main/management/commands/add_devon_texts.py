from django.core.management.base import BaseCommand
from main.models import DevonCategory, DevonGroup, DevonText
from docx import Document
import os

class Command(BaseCommand):
    help = "Word faylidan Devon matnlarini yuklash"

    def handle(self, *args, **kwargs):
        try:
            category = DevonCategory.objects.get(name="Masnaviy")
        except DevonCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR('Kategoriya "Masnaviy" topilmadi.'))
            return

        doc_path = r"C:\Users\acer\Downloads\fard.docx"
        if not os.path.exists(doc_path):
            self.stdout.write(self.style.ERROR(f'Fayl topilmadi: {doc_path}'))
            return

        # First, delete existing texts to avoid duplicates
        DevonText.objects.filter(group__category=category).delete()

        document = Document(doc_path)
        paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
        
        current_group = None
        line_pair = []
        
        for para in paragraphs:
            # Skip empty lines
            if not para:
                continue
                
            # If line starts with a number (like "1."), it's a new group
            if para[0].isdigit() and '.' in para[:3]:
                # If we have a previous group with incomplete lines, log it
                if line_pair:
                    self.stdout.write(self.style.WARNING(f'Guruh {current_group.name if current_group else "?"} uchun faqat bitta qator topildi'))
                    line_pair = []
                
                # Get the number from the line (e.g., "1." -> 1)
                group_number = int(para.split('.')[0])
                try:
                    current_group = DevonGroup.objects.get(category=category, name=str(group_number))
                    # Remove the number and dot from the start of the line
                    cleaned_line = para.split('.', 1)[1].strip()
                    line_pair = [cleaned_line]
                    self.stdout.write(self.style.SUCCESS(f'Guruh topildi: {group_number}'))
                except DevonGroup.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Guruh topilmadi: {group_number}'))
                    current_group = None
                    line_pair = []
            elif current_group and len(line_pair) < 2:
                line_pair.append(para)
                
                # If we have a complete pair, save it
                if len(line_pair) == 2:
                    text_content = '\n'.join(line_pair)
                    DevonText.objects.create(
                        group=current_group,
                        text=text_content,
                        order=1
                    )
                    self.stdout.write(self.style.SUCCESS(f'Guruh {current_group.name} uchun matn qo\'shildi: \n{text_content}'))
                    line_pair = []

        # Check if there's an incomplete pair at the end
        if line_pair:
            self.stdout.write(self.style.WARNING(f'Guruh {current_group.name if current_group else "?"} uchun faqat bitta qator topildi'))

        self.stdout.write(self.style.SUCCESS('Devon matnlari muvaffaqiyatli yuklandi!'))
