from django.db import models

class AuthorInfo(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()
    memories = models.TextField()

    def __str__(self):
        return self.name



class Baburnoma(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    pdf_file = models.FileField(upload_to='boburnoma/', verbose_name="PDF fayl")
    text_content = models.TextField(verbose_name="Qidiruv uchun matn", help_text="Bu matn faqat qidiruv uchun ishlatiladi", blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuklangan vaqt")

    class Meta:
        verbose_name = "Boburnoma"
        verbose_name_plural = "Boburnoma"

    def __str__(self):
        return self.title

class DevonCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nomi")
    image = models.ImageField(upload_to='devon/categories/', verbose_name="Rasm")
    count = models.IntegerField(default=0, verbose_name="Soni")
    order = models.IntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        verbose_name = "Devon kategoriyasi"
        verbose_name_plural = "Devon kategoriyalari"
        ordering = ['order']

    def __str__(self):
        return self.name

class DevonGroup(models.Model):
    category = models.ForeignKey(DevonCategory, on_delete=models.CASCADE, related_name='groups', verbose_name="Kategoriya")
    name = models.CharField(max_length=200, verbose_name="Nomi")
    order = models.IntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        verbose_name = "Devon guruhi"
        verbose_name_plural = "Devon guruhlari"
        ordering = ['order']

    def __str__(self):
        return f'{self.category.name} - {self.name}'

class DevonText(models.Model):
    group = models.ForeignKey(DevonGroup, on_delete=models.CASCADE, related_name='texts', verbose_name="Guruh")
    text = models.TextField(verbose_name="Matn")
    order = models.IntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        verbose_name = "Devon matni"
        verbose_name_plural = "Devon matnlari"
        ordering = ['order']

    def __str__(self):
        return f'{self.group.name} - {self.text[:50]}...'

class AdminContact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f'Message from {self.name}'

class Boburnoma(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    pdf_file = models.FileField(upload_to='boburnoma/', verbose_name="PDF fayl")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuklangan vaqt")

    class Meta:
        verbose_name = "Boburnoma"
        verbose_name_plural = "Boburnoma"

    def __str__(self):
        return self.title

class DevonItem(models.Model):
    category = models.ForeignKey(DevonCategory, on_delete=models.CASCADE, related_name='items', verbose_name="Kategoriya")
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Matn")
    order = models.IntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        verbose_name = "Devon matni"
        verbose_name_plural = "Devon matnlari"
        ordering = ['order']

    def __str__(self):
        return f"{self.category.name} - {self.title}"

class Work(models.Model):
    category = models.ForeignKey(DevonCategory, related_name='works', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Dictionary(models.Model):
    word = models.CharField(max_length=100, verbose_name="So'z")
    description = models.TextField(verbose_name="Izoh")

    class Meta:
        verbose_name = "Lug'at"
        verbose_name_plural = "Lug'atlar"
        ordering = ['word']
        indexes = [
            models.Index(fields=['word']),
        ]

    def save(self, *args, **kwargs):
        self.word = self.word.strip()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.word

    @staticmethod
    def get_ordered_queryset():
        """O'zbek alifbosi tartibida so'zlarni qaytaradi"""
        uzbek_alphabet = 'a b d e f g h i j k l m n o p q r s t u v x y z oʻ gʻ sh ch ng'

        def uzbek_order(word):
            order_dict = {char: i for i, char in enumerate(uzbek_alphabet)}
            return [order_dict.get(c, len(uzbek_alphabet)) for c in word.lower()]

        queryset = Dictionary.objects.all()
        return sorted(queryset, key=lambda x: uzbek_order(x.word))
