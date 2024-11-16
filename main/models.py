from django.db import models

class AuthorInfo(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()
    memories = models.TextField()

    def __str__(self):
        return self.name

class Baburnoma(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    pdf_file = models.FileField(upload_to='boburnoma_pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DivanCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='divan_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class DivanGroup(models.Model):
    category = models.ForeignKey(DivanCategory,related_name='groups', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.category.name} - {self.name}'



class DivanText(models.Model):
    devon_group = models.ForeignKey(DivanGroup,related_name='texts', on_delete=models.CASCADE,null = True)
    text = models.TextField()

    def __str__(self):
        if self.devon_group:
            devon_group_name = self.devon_group.name
        else:
            devon_group_name = 'No Group'
        return f'{devon_group_name} - {self.text}'

class AdminContact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f'Message from {self.name}'







