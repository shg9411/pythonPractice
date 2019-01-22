from django.db import models
from datetime import datetime

class Board(models.Model):
    idx = models.AutoField(primary_key=True)
    writer = models.CharField(null = False, max_length=50)
    title = models.CharField(null = False, max_length=120)
    hit = models.IntegerField(default=0) #조회수
    content = models.TextField(null = False) #textfield는 제한 길이 없음
    post_date = models.DateTimeField(default=datetime.now,blank=True)
    filename=models.CharField(null=True,blank=True,default="",max_length=500)
    filesize=models.IntegerField(default=0)
    down=models.IntegerField(default=0) #다운로드 횟수

    def hit_up(self): #조회수 증가 함수
        self.hit += 1
    def down_up(self): #다운수 증가 함수
        self.down += 1
        
class Comment(models.Model): #댓글 테이블
    idx = models.AutoField(primary_key=True)
    board_idx = models.IntegerField(null = False)
    writer = models.CharField(null=False,max_length=50)
    content=models.TextField(null=False)
    post_date = models.DateTimeField(default=datetime.now, blank=True)

