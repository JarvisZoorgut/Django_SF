from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.authorUser} / Рейтинг: {self.ratingAuthor}'

    def uptate_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat = postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'    


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    postCategory = models.ManyToManyField(Category, through='PostCategory')

    CATEGORY_CHOICES = (
        ('NW', 'Новость'),
        ('AR', 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.categoryType} / {self.title}'    
    
    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

    def preview(self):
        return f'self.text[0:123]... / Рейтинг: self.rating'
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.id})

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.categoryThrough} / {self.postThrough.title}'    

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

