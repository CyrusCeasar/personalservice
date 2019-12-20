from django.db import models


# Create your models here.


class TranslateRecord(models.Model):
    words_text = models.CharField(max_length=50, primary_key=True)
    last_quest_date = models.DateTimeField('date published')
    quest_num = models.IntegerField(default=1)
    src_content = models.TextField()
    display_content = models.TextField()
    is_remembered = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.words_text + "---" + self.display_content
