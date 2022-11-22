from django.shortcuts import render,redirect
from .models import Portfolio

from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

# Create your views here.
class UserSignup(FormView):
	template_name = 'app/signup.html'
	form_class = UserCreationForm
	redirect_authenticated_user = True
	success_url = reverse_lazy('login')

	def form_valid(self, form):
		user = form.save()
		if user is not None:
			login(self.request, user)
		return super(UserSignup, self).form_valid(form)

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('pfllist')
		return super(UserSignup, self).get(*args, **kwargs)


class UserLogin(LoginView):
	template_name = 'app/signin.html'
	fields = '__all__'
	redirect_authenticated_user = True

	def get_success_url(self):
		return reverse_lazy('pfllist')


class PortfolioList(LoginRequiredMixin,View):
	def get(self,request):
		account = User.objects.get(username=request.user)
		context = {'portfolio':account}
		return render(request,'app/home.html',context)


class PortfolioDelete(LoginRequiredMixin,DeleteView):
	model = Portfolio
	success_url = reverse_lazy('pfllist')


class PortfolioCreate(LoginRequiredMixin,View):

	def get(self,request):
		return render(request,'app/portfolio_create_form.html')

	def post(self,request):
		user = User.objects.get(username=request.user)
		pfl_name = request.POST.get('portfolio_name')
		user.portfolio_set.create(name=pfl_name)
		my_object = user.portfolio_set.get(name=pfl_name).id
		return redirect('pfldetail', my_object)


class PortfolioDetail(LoginRequiredMixin,DetailView):
	model = Portfolio
	context_object_name = 'pfl'

	def get(self,*args,**kwargs):
		return super(PortfolioDetail, self).get(*args,**kwargs)

	def post(self,*args,**kwargs):
		return super(PortfolioDetail, self).get(*args,**kwargs)

	def dispatch(self,request,pk,*args,**kwargs):
		dbt_trans, dbt_amt = request.POST.get('dbt'), request.POST.get('dbt-amt')
		cdt_trans, cdt_amt = request.POST.get('cdt'), request.POST.get('cdt-amt')
		trans_date = request.POST.get('trans_date')
		date = request.POST.get('trans-date')
		pfl = self.model.objects.get(id=pk)
		if self.request.POST.get('save'):
			try:
				if dbt_trans and dbt_amt and cdt_trans and cdt_amt != None:
					dbt_whole_trans = pfl.debit_set.create(dbt=dbt_trans, amount=dbt_amt, date=trans_date)
					cdt_whole_trans = pfl.credit_set.create(cdt=cdt_trans, amount=cdt_amt, date=trans_date)
					dbt_whole_trans.save()
					cdt_whole_trans.save()
			except:
				return super(PortfolioDetail, self).dispatch(request,*args,**kwargs)


		elif request.POST.get('delete_this'):
			trans_index = request.POST.get('delete_this')
			pfl.debit_set.get(id=trans_index).delete()

		return super(PortfolioDetail, self).dispatch(request,*args,**kwargs)

