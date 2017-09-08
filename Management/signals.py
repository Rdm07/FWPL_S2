from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.utils.encoding import smart_str
from itertools import chain

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

from Management.models import *

@receiver(post_save, sender=SinglePlayerTeamAnswerSet, dispatch_uid="SPTA Points")
def allocate_points_SPTA(sender, **kwargs):
	instance = kwargs['instance']
	question = instance.for_question
	answer_list = SinglePlayerTeamAnswer.objects.filter(for_question=question)
	for a in answer_list:
		if (a.points == 0 or a.points == -2):
			if a.answer.lower() == instance.answer.lower():
				if a.bonus == True:
					a.points = 2
					a.save()
				else:
					a.points = 1
					a.save()
			else:
				if a.bonus == True:
					a.points = -2
					a.save()
				else:
					a.points = 0
					a.save()


@receiver(post_save, sender=YesNoAnswerSet, dispatch_uid="YNA Points")
def allocate_points_YNA(sender, **kwargs):
	instance = kwargs['instance']
	question = instance.for_question
	answer_list = YesNoAnswer.objects.filter(for_question=question)
	for a in answer_list:
		if (a.points == 0 or a.points == -2):
			if a.answer == instance.answer:
				if a.bonus == True:
					a.points = 2
					a.save()
				else:
					a.points = 1
					a.save()
			else:
				if a.bonus == True:
					a.points = -2
					a.save()
				else:
					a.points = 0
					a.save()
			
@receiver(post_save, sender=WinDrawLoseAnswerSet, dispatch_uid="WDLA Points")
def allocate_points_WDLA(sender, **kwargs):
	instance = kwargs['instance']
	question = instance.for_question
	answer_list = WinDrawLoseAnswer.objects.filter(for_question=question)
	for a in answer_list:
		if (a.points == 0 or a.points == -2):
			if a.answer == instance.answer:
				if a.bonus == True:
					a.points = 2
					a.save()
				else:
					a.points = 1
					a.save()
			else:
				if a.bonus == True:
					a.points = -2
					a.save()
				else:
					a.points = 0
					a.save()

@receiver(post_save, sender=ScorelineAnswerSet, dispatch_uid="SA Points")
def allocate_points_SA(sender, **kwargs):
	instance = kwargs['instance']
	question = instance.for_question
	answer_list = ScorelineAnswer.objects.filter(for_question=question)
	for a in answer_list:
		if (a.points == 0 or a.points == -2):
			if (a.home_team_score == instance.home_team_score and a.away_team_score == instance.away_team_score):
				if a.bonus == True:
					a.points = 2
					a.save()
				else:
					a.points = 1
					a.save()
			else:
				if a.bonus == True:
					a.points = -2
					a.save()
				else:
					a.points = 0
					a.save()

@receiver(post_save, sender=SingleIntegerAnswerSet, dispatch_uid="SIA Points")
def allocate_point_SIA(sender, **kwargs):
	instance = kwargs['instance']
	question = instance.for_question
	answer_list = SingleIntegerAnswer.objects.filter(for_question=question)
	margin = question.margin
	for a in answer_list:
		if (a.points == 0 or a.points == -2):
			if ((instance.answer - margin) <= a.answer <= (instance.answer + margin)):
				if a.bonus == True:
					a.points = 2
				else:
					a.points = 1
				a.save()
			else:
				if a.bonus == True:
					a.points = -2
				else:
					a.points = 0
				a.save()

@receiver(post_save, sender=TeamAndValueAnswerSet, dispatch_uid="TAVA Points")
def allocate_points_TAVA(sender, **kwargs):
	instance = kwargs['instance']
	question = instance.for_question
	answer_list = TeamAndValueAnswer.objects.filter(for_question=question)
	margin = question.margin
	for a in answer_list:
		if (a.points == 0 or a.points == -2):
			if (a.team.lower() == instance.team.lower() and (instance.value - margin) <= a.value <= (instance.value + margin)):
				if a.bonus == True:
					a.points = 2
				else:
					a.points = 1
				a.save()
			else:
				if a.bonus == True:
					a.points = -2
				else:
					a.points = 0
				a.save()

@receiver(post_save, sender=Matchday, dispatch_uid="Matchday Points")
def allocate_matchday_points(sender, **kwargs):
	instance = kwargs['instance']
	if instance.deadline_passed == True:

		users = Profile.objects.exclude(username = 'admin').order_by('first_name')
		for u in users:
			matchdaybonuscount = MatchdayBonus.objects.filter(for_matchday = instance, for_player = u).count()
			SPTA_list = SinglePlayerTeamAnswer.objects.filter(by_player = u, for_question__for_matchday = instance)
			YNA_list = YesNoAnswer.objects.filter(by_player = u, for_question__for_matchday = instance)
			WDLA_list = WinDrawLoseAnswer.objects.filter(by_player = u, for_question__for_matchday = instance)
			SA_list = ScorelineAnswer.objects.filter(by_player = u, for_question__for_matchday = instance)
			SIA_list = SingleIntegerAnswer.objects.filter(by_player = u, for_question__for_matchday = instance)
			TAVA_list = TeamAndValueAnswer.objects.filter(by_player = u, for_question__for_matchday = instance)
			a_list = list(chain(SPTA_list, YNA_list, WDLA_list, SA_list, SIA_list, TAVA_list))
			bonus_exists = 0
			for a in a_list:
				if a.bonus == True:
					bonus_exists = 1

			if bonus_exists == 1:
				if matchdaybonuscount == 0:
					matchdaybonusobject = MatchdayBonus(bonus_exists = True, bonus_points = 0, for_matchday = instance, for_player = u)
					matchdaybonusobject.save()
			elif  bonus_exists == 0:
				if matchdaybonuscount == 0:
					print('here')
					matchdaybonusobject = MatchdayBonus(bonus_exists = False, bonus_points = -2, for_matchday = instance, for_player = u)
					matchdaybonusobject.save()