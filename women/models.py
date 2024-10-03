from django.db import models
from django.shortcuts import reverse


# from autoslug import AutoSlugField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class TagPost(models.Model):
    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'

    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.tag

    def get_absolute_url(self) -> str:
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('category', kwargs={'cat_slug': self.slug})


class Husband(models.Model):
    class Meta:
        verbose_name = 'Муж'
        verbose_name_plural = 'Мужья'

    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(default=0, blank=True)

    def __str__(self) -> str:
        return self.name


class Women(models.Model):
    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['title', '-time_create']
        indexes = [
            models.Index(fields=['title', '-time_create']),
        ]

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name='Опубликовано')
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(TagPost, blank=True, related_name='womens', verbose_name='Метки')
    husband = models.OneToOneField(Husband, on_delete=models.SET_NULL, null=True, blank=True, related_name='wife',
                                   verbose_name='Муж')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('post', kwargs={'post_slug': self.slug})
