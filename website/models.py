from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files.base import ContentFile
from gtts import gTTS

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)  

    def __str__(self):
        return self.name

class Word(models.Model):
    russian_word = models.CharField(max_length=100)
    english_word = models.CharField(max_length=100, default="No translation provided")
    distractors = models.CharField(max_length=300, default='Add words')  

    def get_distractors_list(self):
        return self.distractors.split() 
    
    def __str__(self):
        return self.russian_word + " - " + self.english_word

class Question(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    correct = models.BooleanField(default=False)  
    
    def __str__(self):
        return str(self.word)

class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    questions = models.ManyToManyField(Question)
    current_question = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.category) if self.category else 'No Category'
    
    
    
class ListeningWord(models.Model):
    word = models.CharField(max_length=100, default="No word provided", blank=True, null=True)
    audio_file = models.FileField(upload_to='listening_words/', blank=True, null=True)
    distractors = models.CharField(max_length=300, default='Add words')

    def get_distractors_list(self):
        return self.distractors.split() 
    
    def save(self, *args, **kwargs):
        if not self.audio_file:
            tts = gTTS(text=self.word, lang='en')
            buf = BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            self.audio_file.save(f"{self.word}.mp3", ContentFile(buf.read()), save=False)
        super().save(*args, **kwargs)

    def __str__(self): 
        return self.word
    
class ListeningQuestion(models.Model):
    word = models.ForeignKey(ListeningWord, on_delete=models.CASCADE, blank=True, null=True)
    completed = models.BooleanField(default=False)
    correct = models.BooleanField(default=False)  
    
    def __str__(self):
        return str(self.word)
    
class ListeningTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    questions = models.ManyToManyField(ListeningQuestion)
    current_question = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.category) if self.category else 'No Category'



class GrammarTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    current_question = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class GrammarQuestion(models.Model):
    test = models.ForeignKey(GrammarTest, related_name='questions', on_delete=models.CASCADE)
    sentence = models.TextField()
    correct_answer = models.CharField(max_length=100)

    def __str__(self):
        return self.sentence

class AnswerOption(models.Model):
    question = models.ForeignKey(GrammarQuestion, related_name='options', on_delete=models.CASCADE)
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word