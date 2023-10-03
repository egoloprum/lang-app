from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(Average_score)
admin.site.register(Selected_Answer)
admin.site.register(Completed_Quiz)
