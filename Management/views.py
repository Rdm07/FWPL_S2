from django.shortcuts import render
import poplib

from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.forms import FileInput
from django.forms.models import modelform_factory
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import get_template
from django.utils import timezone
from django.utils.encoding import smart_str
from django.views.generic import (View, ListView, TemplateView, DetailView, CreateView, UpdateView)
from itertools import chain
from django.views.generic.edit import FormView, ModelFormMixin

from Management import forms
from Management.forms import *

def handler400(request):
	return render(request, 'Management/400.html')


def handler403(request):
	return render(request, 'Management/403.html')


def handler404(request):
	return render(request, 'Management/404.html')


def handler500(request):
	return render(request, 'Management/500.html')


def handler503(request):
	return render(request, 'Management/503.html')


class Login(View):
	template_name = 'Management/login.html'

	def get(self, request):
		if request.user.is_authenticated():
			return redirect('home')
		form_my = LoginForm()
		return render(request, self.template_name, dict(form=form_my))

	def post(self, request):
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = auth.authenticate(username=username, password=password)
			if user is not None:
				auth.login(request, user)
				return redirect('home')
			else:
				return render(request, self.template_name, dict(form=form))
		else:
			return render(request, self.template_name, dict(form=form))

class Logout(View):
	def get(self, request):
		auth.logout(request)
		return redirect('login')

# class RedirectHome(View):
# 	def get(self, request):
# 		return redirect('login')

class Home(LoginRequiredMixin, TemplateView):
	login_url = reverse_lazy('login')
	template_name = 'Management/home.html'

	def get_context_data(self, **kwargs):
		context = super(Home, self).get_context_data(**kwargs)
		context['user'] = Profile.objects.get(username=self.request.user.username)
		m_count = Matchday.objects.all().count()
		context['m_count'] = m_count
		return context

class Register(View):
	template_name = 'Management/register.html'

	def get(self, request):
		form_my = ProfileForm()
		return render(request, self.template_name, dict(form=form_my))

	def post(self, request):
		form = ProfileForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('register-confirm')
		else:
			return render(request, self.template_name, dict(form=form))

class RegisterConfirm(TemplateView):
	template_name = 'Management/register_confirm.html'

class Matchdays(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('login')
	template_name = 'Management/matchdays.html'
	context_object_name = 'matchday'

	def get_queryset(self, **kwargs):
		pk = self.kwargs['pk']
		return Matchday.objects.get(day = pk)

	# AJAX Script from Narendra

	def get_context_data(self, **kwargs):
		context = super(Matchdays, self).get_context_data(**kwargs)
		context['user'] = Profile.objects.get(username=self.request.user.username)
		pk = self.kwargs['pk']
		user = Profile.objects.get(username=self.request.user.username)
		m = Matchday.objects.get(day = pk)
		m_all = Matchday.objects.all()

		m_count = Matchday.objects.all().count()
		m_prv = m.day - 1
		m_next = m.day + 1

		context['m_count'] = m_count
		context['m_prv'] = m_prv
		context['m_next'] = m_next
		context['m_all'] = m_all

		q_list = Question.objects.filter(for_matchday = m).order_by('q_number')
		q_count = q_list.count()
		context['q_list'] = q_list
		context['q_count'] = q_count

		SPTAS_list = SinglePlayerTeamAnswerSet.objects.filter(for_question__for_matchday__day = pk)
		YNAS_list = YesNoAnswerSet.objects.filter(for_question__for_matchday__day = pk)
		WDLAS_list = WinDrawLoseAnswerSet.objects.filter(for_question__for_matchday__day = pk)
		SAS_list = ScorelineAnswerSet.objects.filter(for_question__for_matchday__day = pk)
		SIAS_list = SingleIntegerAnswerSet.objects.filter(for_question__for_matchday__day = pk)
		TAVAS_list = TeamAndValueAnswerSet.objects.filter(for_question__for_matchday__day = pk)
		aset_list = list(chain(SPTAS_list, YNAS_list, WDLAS_list, SAS_list, SIAS_list, TAVAS_list))
		context['aset_list'] = aset_list

		SPTA_list = SinglePlayerTeamAnswer.objects.filter(by_player = user, for_question__for_matchday__day = pk)
		YNA_list = YesNoAnswer.objects.filter(by_player = user, for_question__for_matchday__day = pk)
		WDLA_list = WinDrawLoseAnswer.objects.filter(by_player = user, for_question__for_matchday__day = pk)
		SA_list = ScorelineAnswer.objects.filter(by_player = user, for_question__for_matchday__day = pk)
		SIA_list = SingleIntegerAnswer.objects.filter(by_player = user, for_question__for_matchday__day = pk)
		TAVA_list = TeamAndValueAnswer.objects.filter(by_player = user, for_question__for_matchday__day = pk)
		a_list = list(chain(SPTA_list, YNA_list, WDLA_list, SA_list, SIA_list, TAVA_list))
		context['a_list'] = a_list

		m_points = 0
		mb_all = MatchdayBonus.objects.filter(for_matchday = m, for_player = user)
		for mb in mb_all:
			m_points = mb.bonus_points

		for a in a_list:
			m_points = m_points + a.points

		context['points'] = m_points

		n = q_list.count()
		exists = [0]*(n+1)
		for q in q_list:
			for a in a_list:
				if a.for_question == q:
					exists[q.q_number] = 1
					break

		context['exists'] = exists
		return context

class MatchdaysUser(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('login')
	template_name = 'Management/matchdays_user.html'
	context_object_name = 'matchday'

	def get_queryset(self, **kwargs):
		pk1 = self.kwargs['pk1']
		return Matchday.objects.get(id = pk1)

	# AJAX Script from Narendra

	def get_context_data(self, **kwargs):
		context = super(MatchdaysUser, self).get_context_data(**kwargs)
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		user = Profile.objects.get(id = pk2)
		context['user'] = user
		m = Matchday.objects.get(id = pk1)
		m_all = Matchday.objects.all()

		m_count = Matchday.objects.all().count()
		m_prv = m.day - 1
		m_next = m.day + 1

		context['m_count'] = m_count
		context['m_prv'] = m_prv
		context['m_next'] = m_next
		context['m_all'] = m_all

		q_list = Question.objects.filter(for_matchday = m).order_by('q_number')
		context['q_list'] = q_list

		SPTAS_list = SinglePlayerTeamAnswerSet.objects.filter(for_question__for_matchday__day = pk1)
		YNAS_list = YesNoAnswerSet.objects.filter(for_question__for_matchday__day = pk1)
		WDLAS_list = WinDrawLoseAnswerSet.objects.filter(for_question__for_matchday__day = pk1)
		SAS_list = ScorelineAnswerSet.objects.filter(for_question__for_matchday__day = pk1)
		SIAS_list = SingleIntegerAnswerSet.objects.filter(for_question__for_matchday__day = pk1)
		TAVAS_list = TeamAndValueAnswerSet.objects.filter(for_question__for_matchday__day = pk1)
		aset_list = list(chain(SPTAS_list, YNAS_list, WDLAS_list, SAS_list, SIAS_list, TAVAS_list))
		context['aset_list'] = aset_list

		SPTA_list = SinglePlayerTeamAnswer.objects.filter(by_player = user, for_question__for_matchday__day = pk1)
		YNA_list = YesNoAnswer.objects.filter(by_player = user, for_question__for_matchday__day = pk1)
		WDLA_list = WinDrawLoseAnswer.objects.filter(by_player = user, for_question__for_matchday__day = pk1)
		SA_list = ScorelineAnswer.objects.filter(by_player = user, for_question__for_matchday__day = pk1)
		SIA_list = SingleIntegerAnswer.objects.filter(by_player = user, for_question__for_matchday__day = pk1)
		TAVA_list = TeamAndValueAnswer.objects.filter(by_player = user, for_question__for_matchday__day = pk1)
		a_list = list(chain(SPTA_list, YNA_list, WDLA_list, SA_list, SIA_list, TAVA_list))
		context['a_list'] = a_list
		m_points = 0
		mb_all = MatchdayBonus.objects.filter(for_matchday = m, for_player = user)
		for mb in mb_all:
			m_points = mb.bonus_points

		for a in a_list:
			m_points = m_points + a.points

		context['points'] = m_points

		n = q_list.count()
		exists = [0]*(n+1)
		for q in q_list:
			for a in a_list:
				if a.for_question == q:
					exists[q.q_number] = 1
					break

		context['exists'] = exists
		return context


class SubmitAnswer(LoginRequiredMixin, CreateView):
	login_url = reverse_lazy('login')
	template_name = 'Management/submitanswer.html'

	def get_form_class(self, **kwargs):
		user = Profile.objects.get(username=self.request.user.username)
		pk = self.kwargs['pk']
		question = Question.objects.get(id = pk)
		SPTA_list = SinglePlayerTeamAnswer.objects.filter(by_player = user, for_question__for_matchday = question.for_matchday)
		YNA_list = YesNoAnswer.objects.filter(by_player = user, for_question__for_matchday = question.for_matchday)
		WDLA_list = WinDrawLoseAnswer.objects.filter(by_player = user, for_question__for_matchday = question.for_matchday)
		SA_list = ScorelineAnswer.objects.filter(by_player = user, for_question__for_matchday = question.for_matchday)
		SIA_list = SingleIntegerAnswer.objects.filter(by_player = user, for_question__for_matchday = question.for_matchday)
		TAVA_list = TeamAndValueAnswer.objects.filter(by_player = user, for_question__for_matchday = question.for_matchday)
		a_list = list(chain(SPTA_list, YNA_list, WDLA_list, SA_list, SIA_list, TAVA_list))

		bonus_count = 0
		for a in a_list:
			if a.bonus == True:
				bonus_count = bonus_count + 1

		if question.bonus_allowed == True:
			if bonus_count == 0:
				if question.answer_type.model == 'singleplayerteamanswer':
					form_class = SPTAForm().__class__
				elif question.answer_type.model == 'yesnoanswer':
					form_class = YNAForm().__class__
				elif question.answer_type.model == 'windrawloseanswer':
					form_class = WDLAForm().__class__
				elif question.answer_type.model == 'scorelineanswer':
					form_class = SAForm().__class__
				elif question.answer_type.model == 'singleintegeranswer':
					form_class = SIAForm().__class__
				elif question.answer_type.model == 'teamandvalueanswer':
					form_class = TAVAForm().__class__
				return form_class

			else:
				if question.answer_type.model == 'singleplayerteamanswer':
					form_class = SPTAForm_NoBonus().__class__
				elif question.answer_type.model == 'yesnoanswer':
					form_class = YNAForm_NoBonus().__class__
				elif question.answer_type.model == 'windrawloseanswer':
					form_class = WDLAForm_NoBonus().__class__
				elif question.answer_type.model == 'scorelineanswer':
					form_class = SAForm_NoBonus().__class__
				elif question.answer_type.model == 'singleintegeranswer':
					form_class = SIAForm_NoBonus().__class__
				elif question.answer_type.model == 'teamandvalueanswer':
					form_class = TAVAForm_NoBonus().__class__
				return form_class
		else:
			if question.answer_type.model == 'singleplayerteamanswer':
				form_class = SPTAForm_NoBonus().__class__
			elif question.answer_type.model == 'yesnoanswer':
				form_class = YNAForm_NoBonus().__class__
			elif question.answer_type.model == 'windrawloseanswer':
				form_class = WDLAForm_NoBonus().__class__
			elif question.answer_type.model == 'scorelineanswer':
				form_class = SAForm_NoBonus().__class__
			elif question.answer_type.model == 'singleintegeranswer':
				form_class = SIAForm_NoBonus().__class__
			elif question.answer_type.model == 'teamandvalueanswer':
				form_class = TAVAForm_NoBonus().__class__
			return form_class

	def get_context_data(self, **kwargs):
		context = super(SubmitAnswer, self).get_context_data(**kwargs)
		pk = self.kwargs['pk']
		question = Question.objects.get(id = pk)
		context['question'] = question
		m_count = Matchday.objects.all().count()
		context['m_count'] = m_count
		return context

	def form_valid(self, form, **kwargs):
		user = Profile.objects.get(username=self.request.user.username)
		pk = self.kwargs['pk']
		question = Question.objects.get(id=pk)
		form.instance.by_player = user
		form.instance.for_question = question
		form.instance.save()
		return super(SubmitAnswer, self).form_valid(form)

	def get_success_url(self, **kwargs):
		user = Profile.objects.get(username=self.request.user.username)
		pk = self.kwargs['pk']
		question = Question.objects.get(id=pk)
		m = question.for_matchday.day
		return reverse('matchdays', kwargs={'pk': m})

class UpdateAnswer(LoginRequiredMixin, UpdateView):
	login_url = reverse_lazy('login')
	template_name = 'Management/updateanswer.html'

	def get_form_class(self, **kwargs):
		user = Profile.objects.get(username=self.request.user.username)
		pk = self.kwargs['pk']
		question = Question.objects.get(id = pk)
		SPTA_list = SinglePlayerTeamAnswer.objects.filter(by_player = user, for_question__for_matchday = question.for_matchday)
		YNA_list = YesNoAnswer.objects.filter(by_player = user, for_question__for_matchday = question.for_matchday)
		WDLA_list = WinDrawLoseAnswer.objects.filter(by_player = user, for_question__for_matchday = question.for_matchday)
		SA_list = ScorelineAnswer.objects.filter(by_player = user, for_question__for_matchday = question.for_matchday)
		SIA_list = SingleIntegerAnswer.objects.filter(by_player = user, for_question__for_matchday = question.for_matchday)
		TAVA_list = TeamAndValueAnswer.objects.filter(by_player = user, for_question__for_matchday = question.for_matchday)
		a_list = list(chain(SPTA_list, YNA_list, WDLA_list, SA_list, SIA_list, TAVA_list))

		bonus_count = 0
		for a in a_list:
			if a.bonus == True:
				bonus_count = bonus_count + 1

		queryset = question.answer_type.model_class().objects.all()
		ans = queryset.get(for_question=question, by_player = user)

		if question.bonus_allowed == True:
			if (bonus_count == 1 and ans.bonus == False):
				if question.answer_type.model == 'singleplayerteamanswer':
					form_class = SPTAForm_NoBonus().__class__
				elif question.answer_type.model == 'yesnoanswer':
					form_class = YNAForm_NoBonus().__class__
				elif question.answer_type.model == 'windrawloseanswer':
					form_class = WDLAForm_NoBonus().__class__
				elif question.answer_type.model == 'scorelineanswer':
					form_class = SAForm_NoBonus().__class__
				elif question.answer_type.model == 'singleintegeranswer':
					form_class = SIAForm_NoBonus().__class__
				elif question.answer_type.model == 'teamandvalueanswer':
					form_class = TAVAForm_NoBonus().__class__
				return form_class

			else:
				if question.answer_type.model == 'singleplayerteamanswer':
					form_class = SPTAForm().__class__
				elif question.answer_type.model == 'yesnoanswer':
					form_class = YNAForm().__class__
				elif question.answer_type.model == 'windrawloseanswer':
					form_class = WDLAForm().__class__
				elif question.answer_type.model == 'scorelineanswer':
					form_class = SAForm().__class__
				elif question.answer_type.model == 'singleintegeranswer':
					form_class = SIAForm().__class__
				elif question.answer_type.model == 'teamandvalueanswer':
					form_class = TAVAForm().__class__
				return form_class
		else:
			if question.answer_type.model == 'singleplayerteamanswer':
				form_class = SPTAForm_NoBonus().__class__
			elif question.answer_type.model == 'yesnoanswer':
				form_class = YNAForm_NoBonus().__class__
			elif question.answer_type.model == 'windrawloseanswer':
				form_class = WDLAForm_NoBonus().__class__
			elif question.answer_type.model == 'scorelineanswer':
				form_class = SAForm_NoBonus().__class__
			elif question.answer_type.model == 'singleintegeranswer':
				form_class = SIAForm_NoBonus().__class__
			elif question.answer_type.model == 'teamandvalueanswer':
				form_class = TAVAForm_NoBonus().__class__
			return form_class

	def get_object(self, **kwargs):
		user = Profile.objects.get(username=self.request.user.username)
		pk = self.kwargs['pk']
		question = Question.objects.get(id = pk)
		queryset = question.answer_type.model_class().objects.all()
		obj = queryset.get(for_question=question, by_player = user)
		return obj

	def get_context_data(self, **kwargs):
		context = super(UpdateAnswer, self).get_context_data(**kwargs)
		pk = self.kwargs['pk']
		question = Question.objects.get(id = pk)
		context['question'] = question
		m_count = Matchday.objects.all().count()
		context['m_count'] = m_count
		return context

	def form_valid(self, form, **kwargs):
		form.instance.save()
		return super(UpdateAnswer, self).form_valid(form)

	def get_success_url(self, **kwargs):
		pk = self.kwargs['pk']
		question = Question.objects.get(id=pk)
		m = question.for_matchday.day
		return reverse('matchdays', kwargs={'pk': m})

class MatchdayPerformance(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('login')
	template_name = 'Management/matchdayperformance.html'
	context_object_name = 'matchday'

	def get_queryset(self, **kwargs):
		pk = self.kwargs['pk']
		return Matchday.objects.get(day = pk)

	# AJAX Script from Narendra

	def get_context_data(self, **kwargs):
		context = super(MatchdayPerformance, self).get_context_data(**kwargs)
		pk = self.kwargs['pk']
		users = Profile.objects.exclude(username = 'admin').order_by('first_name')
		m = Matchday.objects.get(day = pk)
		m_all = Matchday.objects.all()

		m_count = Matchday.objects.all().count()
		m_prv = m.day - 1
		m_next = m.day + 1

		context['m_count'] = m_count
		context['m_prv'] = m_prv
		context['m_next'] = m_next
		context['m_all'] = m_all
		context['matchday'] = m

		SPTA_list = SinglePlayerTeamAnswer.objects.filter(for_question__for_matchday__day = pk)
		YNA_list = YesNoAnswer.objects.filter(for_question__for_matchday__day = pk)
		WDLA_list = WinDrawLoseAnswer.objects.filter(for_question__for_matchday__day = pk)
		SA_list = ScorelineAnswer.objects.filter(for_question__for_matchday__day = pk)
		SIA_list = SingleIntegerAnswer.objects.filter(for_question__for_matchday__day = pk)
		TAVA_list = TeamAndValueAnswer.objects.filter(for_question__for_matchday__day = pk)
		a_list = list(chain(SPTA_list, YNA_list, WDLA_list, SA_list, SIA_list, TAVA_list))

		points_user = []
		user_all = []
		for u in users:
			user_all.append(u)
			mb_all = MatchdayBonus.objects.filter(for_matchday = m, for_player = u)
			points_u = 0
			for mb in mb_all:
				points_u = mb.bonus_points

			for a in a_list:
				if a.by_player == u:
					points_u = points_u + a.points
			points_user.append(points_u)

		zip_list = zip(user_all, points_user)
		context['zip_list'] = zip_list
		return context

class LeagueTable(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('login')
	template_name = 'Management/leaguetable.html'
	context_object_name = 'total_users'

	def get_queryset(self, **kwargs):
		users = Profile.objects.exclude(username = 'admin')
		n = users.count()
		return n

	def get_context_data(self, **kwargs):
		context = super(LeagueTable, self).get_context_data(**kwargs)
		users = Profile.objects.exclude(username = 'admin').order_by('first_name')
		n = users.count()
		m_all = Matchday.objects.all()
		context['total_users'] = n
		m_count = Matchday.objects.all().count()
		context['m_count'] = m_count

		SPTA_list = SinglePlayerTeamAnswer.objects.all()
		YNA_list = YesNoAnswer.objects.all()
		WDLA_list = WinDrawLoseAnswer.objects.all()
		SA_list = ScorelineAnswer.objects.all()
		SIA_list = SingleIntegerAnswer.objects.all()
		TAVA_list = TeamAndValueAnswer.objects.all()
		a_list = list(chain(SPTA_list, YNA_list, WDLA_list, SA_list, SIA_list, TAVA_list))

		points_user = []
		user_all = []
		for u in users:
			user_all.append(u)
			points_u = 0
			for m in m_all:
				mb_all = MatchdayBonus.objects.filter(for_matchday = m, for_player = u)
				for mb in mb_all:
					points_u = points_u + mb.bonus_points

			for a in a_list:
				if a.by_player == u:
					points_u = points_u + a.points
			points_user.append(points_u)

		points_user, user_all = (list(x) for x in zip(*sorted(zip(points_user, user_all), reverse=True)))

		ranks=[]
		for p in points_user:
			rank_given = 0
			p_given = 0
			if points_user.index(p) == 0:
				rank_given = 1
				p_given = p
				ranks.append(rank_given)
			else:
				if p_given == p:
					ranks.append(rank_given)
				else:
					p_given = p
					rank_given = points_user.index(p) + 1
					ranks.append(rank_given)

		zip_list = zip(user_all, points_user, ranks)

		context['zip_list'] = zip_list
		return context

