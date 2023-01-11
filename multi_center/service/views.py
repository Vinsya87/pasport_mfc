from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from service.models import Extradition, Service

from .forms import ExtraditionForm, ExtraReviewForm, ServiceForm


def paginator_page(request, page_pagi):
    paginator = Paginator(page_pagi, settings.PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


class Manager:
    """Вывод данных для менеджера"""

    def manager(self, request):
        context = {}
        form_extra = ExtraReviewForm(
            self.request.POST or None
        )
        page_service = paginator_page(request, Service.objects.all())
        page_extra = paginator_page(request, Extradition.objects.all())
        context.update(
            page_service=page_service,
            page_extra=page_extra,
            form_extra=form_extra
            )
        return context


class UserService:
    """Вывод данных для пользователя"""

    def user(self, request):
        form_one = ServiceForm(
            self.request.POST or None, files=self.request.FILES
        )
        form_two = ExtraditionForm(
            self.request.POST or None, files=self.request.FILES
        )
        customer_service = Service.objects.filter(author=self.request.user)
        extra_service = Extradition.objects.filter(author=self.request.user)
        context = {
            "form_one": form_one,
            "form_two": form_two,
            "customer_service": customer_service,
            "extra_service": extra_service,
        }
        if customer_service:
            customer_service_last = customer_service.latest('pub_date')
            context.update(
                customer_service_last=customer_service_last)
        if extra_service:
            extra_service_last = extra_service.latest('pub_date')
            context.update(
                extra_service_last=extra_service_last)
                
        return context


class IndexView(Manager, UserService, ListView):
    """Формирование главной страницы"""

    model = Service
    template_name = "service/index.html"

    # def get_queryset(self):
    #     queryset = Extradition.objects.all()
    #     return queryset

    def get_context_data(self):
        if not self.request.user.is_authenticated:
            context = {}
        elif self.request.user.is_user:
            context = self.user(self.request)
        else:
            context = self.manager(self.request)
        return context


class SearchResultsView(ListView):
    """Поиск"""
    template_name = "service/index.html"

    def get_queryset(self):
        if self.request.GET:
            if 'q_extra' in self.request.GET:
                # передача контекста в шаблон
                self.context_object_name = "page_extra"
                # получение информации из запроса
                query = self.request.GET.get("q_extra")
                self.model = Extradition
            elif 'q_service' in self.request.GET:
                self.context_object_name = "page_service"
                query = self.request.GET.get("q_service")
                self.model = Service
        object_list = self.model.objects.filter(
            Q(fio_user__icontains=query) | Q(fio_mother__icontains=query)
        )
        return object_list


class FilterExtraView(ListView):
    """Фильтр"""
    template_name = "service/index.html"
    context_object_name = "page_extra"
    model = Extradition
    queryset = Extradition.objects.order_by('-fio_user')

    def get_queryset(self):
        if self.request.GET:
            if 'f_extra' in self.request.GET:
                self.queryset = Extradition.objects.order_by('fio_user')
        return self.queryset


class FilterServiceView(ListView):
    template_name = "service/index.html"
    context_object_name = "page_service"
    model = Service
    queryset = Service.objects.order_by('-fio_user')

    def get_queryset(self):
        if self.request.GET:
            if 'f_extra' in self.request.GET:
                self.queryset = Service.objects.order_by('fio_user')
        return self.queryset


@login_required
def service_create(request):
    """Форма получения паспорта"""
    form = ServiceForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
    else:
        return HttpResponse("Invalid data")
        # return redirect('posts:profile', username=post.author)
    return render(request, "service/create_service.html", {"form": form})


@login_required
def extra_create(request):
    """Форма выдачи паспорта"""
    form = ExtraditionForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
    else:
        return HttpResponse("Invalid data")
    return render(request, "service/create_service.html", {"form": form})


@login_required
def review_service_yes(request, post_id):
    model = Service
    return review_yes(request, post_id, model)


@login_required
def review_service_no(request, post_id):
    model = Service
    form = ExtraReviewForm
    return review_no(request, post_id, model, form)

@login_required
def extradite_extra_yes(request, post_id):
    model = Extradition
    return extradite_yes(request, post_id, model)


@login_required
def review_extra_yes(request, post_id):
    model = Extradition
    return review_yes(request, post_id, model)


@login_required
def extradite_service_yes(request, post_id):
    model = Service
    return extradite_yes(request, post_id, model)


@login_required
def review_extra_no(request, post_id):
    model = Extradition
    form = ExtraReviewForm
    return review_no(request, post_id, model, form)


def extradite_yes(request, post_id, model):
    """Добавляем статус Выдано"""
    # получаем нужную нам запись id берется из запроса
    post = get_object_or_404(model, pk=post_id)
    if (request.POST and (
        "_extradite_yes" in request.POST) and
       (request.user.is_manager) and
       (post.review == "Выполнено")):
        post.review = "Выдано"
        post.save()
    return redirect(request.META.get("HTTP_REFERER"))


def review_yes(request, post_id, model):
    """Добавляем статус Выполнено"""
    # получаем нужную нам запись id берется из запроса
    post = get_object_or_404(model, pk=post_id)
    if (request.POST and (
        "_review_yes" in request.POST) and
       (request.user.is_manager) and
       (post.review == "В обработке")):
        post.review = "Выполнено"
        post.save()
    return redirect(request.META.get("HTTP_REFERER"))


def review_no(request, post_id, model, form):
    """Добавляем статус Отказано"""
    # получаем нужную нам запись id берется из запроса
    post = get_object_or_404(model, pk=post_id)
    form = form(request.POST or None)
    if form.is_valid():
        post.failure = form.cleaned_data["failure"]
        post.save()
    if (request.POST and
       ("_review_yes" in request.POST) and
       (request.user.is_manager)
       and (post.review == "В обработке")):
        post.review = "Отказано"
        post.save()
    return redirect(request.META.get("HTTP_REFERER"))
