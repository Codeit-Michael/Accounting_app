from django.urls import path
from .views import UserSignup, UserLogin, PortfolioCreate, PortfolioList, PortfolioDetail, PortfolioDelete#,  PersonUpdate
from django.contrib.auth.views import LogoutView

urlpatterns = [
	path('signup/', UserSignup.as_view(), name='signup'),
	path('login/', UserLogin.as_view(), name='login'),
	path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
	path('pfl-create/', PortfolioCreate.as_view(), name='pflcreate'),
	path('', PortfolioList.as_view(), name='pfllist'),
	path('pfl-detail/pk=<int:pk>', PortfolioDetail.as_view(), name='pfldetail'),
# 	path('person-update/pk=<int:pk>', PersonUpdate.as_view(), name='personupdate'),
	path('pfl-delete/pk=<int:pk>', PortfolioDelete.as_view(), name='pfldelete'),
]