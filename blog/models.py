from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, User


class Album(models.Model):
    name = models.CharField(max_length=254, verbose_name='Album name')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    published = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Albums'
        ordering = ['-published']

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag = models.CharField(max_length=100, verbose_name='Tag name', unique=True)

    class Meta:
        verbose_name_plural = 'Tags'
        ordering = ('tag',)

    def __str__(self):
        return self.name


class Photo(models.Model):
    name = models.CharField(max_length=75, db_index=True)
    user = models.ForeignKey(User, related_name='photo_created', default=0, on_delete=models.CASCADE)
    photo = models.ImageField()
    url = models.URLField(default=0)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    album_id = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos',
                                 related_query_name='photos')
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True,
                            blank=True, related_name='photos',
                            related_query_name='photos'
                            )
    published = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Photos'
        ordering = ['-published']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Photo, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('photo:detail', agrs=[self.id, self.slug])


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=254)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    text = models.TextField()
    photo = models.ForeignKey(Photo, default=0, on_delete=models.CASCADE)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    like = models.ManyToManyField(User, related_name='photos_like', blank=True)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

