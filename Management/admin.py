from django.contrib import admin
from django.utils import timezone

# Register your models here.

from .models import *

admin.site.site_header = 'FWPL Site Administration'

class QuestionAdmin(admin.ModelAdmin):
	model = Question
	list_display = ('q_number', 'for_matchday')

class SPTAAdmin(admin.ModelAdmin):
	model = SinglePlayerTeamAnswer
	list_display = ('for_question', 'by_player')

class SPTASAdmin(admin.ModelAdmin):
	model = SinglePlayerTeamAnswerSet
	list_display = ('for_question', 'answer')

class YNAAdmin(admin.ModelAdmin):
	model = YesNoAnswer
	list_display = ('for_question', 'by_player')

class YNASAdmin(admin.ModelAdmin):
	model = YesNoAnswerSet
	list_display = ('for_question', 'answer')

class WDLAAdmin(admin.ModelAdmin):
	model = WinDrawLoseAnswer
	list_display = ('for_question', 'by_player')

class WDLASAdmin(admin.ModelAdmin):
	model = WinDrawLoseAnswerSet
	list_display = ('for_question', 'answer')

class SAAdmin(admin.ModelAdmin):
	model = ScorelineAnswer
	list_display = ('for_question', 'by_player')

class SASAdmin(admin.ModelAdmin):
	model = ScorelineAnswerSet
	list_display = ('for_question', 'home_team_score')

class SIAAdmin(admin.ModelAdmin):
	model = SingleIntegerAnswer
	list_display = ('for_question', 'by_player')

class SIASAdmin(admin.ModelAdmin):
	model = SingleIntegerAnswerSet
	list_display = ('for_question', 'answer')

class TAVAAdmin(admin.ModelAdmin):
	model = TeamAndValueAnswer
	list_display = ('for_question', 'by_player')

class TAVASAdmin(admin.ModelAdmin):
	model = TeamAndValueAnswerSet
	list_display = ('for_question', 'team')


admin.site.register(Matchday)
admin.site.register(MatchdayBonus)
admin.site.register(Question, QuestionAdmin)

admin.site.register(SinglePlayerTeamAnswer, SPTAAdmin)
admin.site.register(YesNoAnswer, YNAAdmin)
admin.site.register(WinDrawLoseAnswer, WDLAAdmin)
admin.site.register(ScorelineAnswer, SAAdmin)
admin.site.register(SingleIntegerAnswer, SIAAdmin)
admin.site.register(TeamAndValueAnswer, TAVAAdmin)

admin.site.register(SinglePlayerTeamAnswerSet, SPTASAdmin)
admin.site.register(YesNoAnswerSet, YNASAdmin)
admin.site.register(WinDrawLoseAnswerSet, WDLASAdmin)
admin.site.register(ScorelineAnswerSet, SASAdmin)
admin.site.register(SingleIntegerAnswerSet, SIASAdmin)
admin.site.register(TeamAndValueAnswerSet, TAVASAdmin)