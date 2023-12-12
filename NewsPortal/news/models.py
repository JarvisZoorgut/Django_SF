from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()
    

class Category(models.Model):
    categoryName = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    authorPost = models.ForeignKey(Author, on_delete=models.CASCADE)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    
    POST_TYPE = (
        ('NW', 'Новость'),
        ('AT', 'Статья'),
    )
    postType = models.CharField(max_length=2, choices=POST_TYPE)
    _datetime = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=128)
    post = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike (self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.title} : {self.post[0:123]} ... // Рейтинг: {self.rating}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    _datetime = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike (self):
        self.rating -= 1
        self.save()
