#___________ НАЧАЛО ИМПОРТА КОМПОНЕНТОВ ______________
from datetime import datetime
import datetime as dt

# для работы с авторизайций пользователей #
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin # специальный миксин для представлений,
from django.contrib.auth.models import User
# работающих тольбко после авторизации. Альтернатива комбинации login_required (method_decorator)

# для работы с почтовой рассылкой
from django.core.mail import EmailMultiAlternatives, mail_managers, send_mail # почтовая рассылка
# c применением шаблона HTML (EmailMultiAlternatives) и функция с обработкой сигналов
from django.template.loader import render_to_string # рендера HTML в строку
from django.db.models.signals import post_init
from django.dispatch import receiver
import django.dispatch as dj_ds

# модели и представления
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Post, Author, Comment, Category, Mail, PostCategory, UserSubcribes

# фильтры и формы
from .filters import PostFilter
from .forms import PostForm, PostCreateForm, SubsribeForm

# загрузка страниц и исключения
from django.shortcuts import reverse, render, redirect
from django.core.exceptions import ObjectDoesNotExist

# импорты для удаления тестовых пользователей (для отработки при создании проекта)
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import EmailAddress
from django.conf import settings

from pprint import pprint
from django.db import models
#___________ КОНЕЦ ИМПОРТА КОМПОНЕНТОВ ______________#


class PostsList(LoginRequiredMixin, ListView): #класс для показа общего списка всех публикаций
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    # ordering = 'create_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'flatpages/news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post'
    paginate_by = 10
    edit_subscribe=None # переменная, сигнализирующая о доступности редактирования подписки пользователем

    def form(self): # метод для присвоения формы, используемой при подписке на категории новостей
        form = SubsribeForm(initial={'category':Category.objects.filter(usersubcribes__subcribe=self.request.user)})
        if self.request.path == '/news/edit_subscribe/':
            form.fields['category'].disabled = False
        return form

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['form'] = self.form
        context['is_not_author']= not self.request.user.groups.filter(name='authors').exists()

        if self.request.path==reverse('edit_subscribe'):
            self.edit_subscribe=True
            context['edit_subscribe'] = self.edit_subscribe
        return context

    def post(self, request, *args, **kwargs):
        subscriptions =[] # список, которая принимает от формы категории,
    # на которые пользователь хочет подписаться
        del_subscriptions=[] # переменная, которая принимает список категорий
                        # на удаление если с них пользователь убирает галочку
        user=request.user
        if request.method=='POST':
            if request.POST ['subscribe']=='Редактировать подписку':
                # здесь требуется код, который бы делал доступной форму для редактирования
                # подписок пользователя
                return redirect('edit_subscribe')
            else:
                form = SubsribeForm(request.POST)
                form.fields['category'].disabled = False
                if form.is_valid(): # если пользователь выбрал хотя бы одну категорию
                    # то формируется список категорий для добавления в БД, если пользователь еще
                    # на неё не подписан
                    subscriptions=[i_category for i_category in form.cleaned_data['category'] if not
                        UserSubcribes.objects.filter(subcribe=user, category=i_category)]

                    # если пользователь снял галочку с категории, на которую подписан,
                    # то она добавится в список на удаление
                    for i_category in Category.objects.all():
                        if (i_category not in form.cleaned_data['category'] and
                                UserSubcribes.objects.filter(subcribe=user, category=i_category)):
                            del_subscriptions.append(i_category)

                else: # если ни одна категория не отмечена, значит все подписки пользователя
                        # добавятся в список на удаление
                    del_subscriptions=[i_category for i_category in Category.objects.all()
                                    if UserSubcribes.objects.filter
                                           (subcribe=user, category=i_category) ]

                # удаление и добавление подписок
                for i_category in del_subscriptions:
                    subscribe_obj=UserSubcribes.objects.get(subcribe=user, category=i_category)
                    subscribe_obj.delete()
                for i_category in subscriptions:
                    UserSubcribes.objects.create(subcribe=user, category=i_category)
                return redirect('main_page')

class PostDetail(LoginRequiredMixin,DetailView): # детальная информация конкретного поста
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs): # модернизация контекста для отображения комментариев
                                                # на отдельной странице поста
        context=super().get_context_data(**kwargs)
        context['comm'] = Comment.objects.filter(post_id=self.kwargs['pk'])
        form=PostForm(initial={'title': self.object.title,
                               'content': self.object.content,
                               'create_time': self.object.create_time,
                               'author': self.object.author,
                               'postType': self.object.postType,
                               'category': Category.objects.filter(postcategory__post=self.object) }
                               )
        form.fields['author'].disabled = True
        form.fields['title'].disabled = True
        form.fields['content'].disabled = True
        form.fields['postType'].disabled = True
        form.fields['category'].disabled = True
        context['form'] = form
        context['id']=self.object.pk # переменная контекста, передающая id поста

    # переменная передающая в контекст информациюЮ обладает ли пользователь правами авторо
        context['is_author']=self.request.user.groups.filter(name='authors').exists()
        return context

class PostFilterView(LoginRequiredMixin, ListView): # класс для отображения фильтра поста на отдельной HTML странице 'search.html'
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'post'
    paginate_by =3

    def get_queryset(self):
        queryset=super().get_queryset()
        self.filter = PostFilter(self.request.GET,queryset)
        return self.filter.qs

    def get_context_data(self,  **kwargs): #добавление в контекст фильтра
        context=super().get_context_data(**kwargs)
        context['filter']=self.filter
        return context

@login_required
@permission_required('news_portal.add_post', raise_exception=True)
def create_post(request): # функция для создания и добавления новой публикации
    delta=datetime.now(dt.timezone.utc)-dt.timedelta(days=1)
    if Post.objects.filter(create_time__gte=delta, author__user=request.user).count()>3:
        return render(request,'posts_limit.html')

    form=PostCreateForm()
    form.fields['author'].queryset=Author.objects.filter(user=request.user)
    # принимающая значение True, если пользователь относится к группе авторов

    if request.method=='POST':
        form=PostCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'flatpages/messages.html', {'state':'Новая публикация добавлена успешно!'})
    return render(request, 'flatpages/edit.html', {'form':form, 'button':'Опубликовать'})

@login_required
@permission_required('news_portal.change_post', raise_exception=True)
def edit_post(request, pk): # функция для редактирования названия и содержания поста
    post = Post.objects.get(pk=pk)
    if post.author.user==request.user: # если публикация принадлежит
        # текущему авторизованному пользователю

        # обладает ли пользователь правами автора публикаций
        is_author= request.user.groups.filter(name='authors').exists()

        form=PostForm(initial={'create_time':post.create_time,
                               'author':post.author,
                               'postType':post.postType,
                               'title': post.title,
                               'content': post.content,
                               'category': Category.objects.filter(postcategory__post=post)
                               })
        form.fields['postType'].disabled = True
        form.fields['author'].disabled = True
        form.fields['category'].queryset = Category.objects.all()
        form.fields['category'].disabled = True
        form.fields['category'].required = False

        if request.method=='POST':
            form=PostForm(request.POST, post)
            form.fields['postType'].required = False
            form.fields['author'].required = False
            form.fields['create_time'].required = False
            form.fields['category'].required = False
            try:
                state = None  # переменная для контекста отображающая сообщение для пользователя о результатах действий
                if form.is_valid():
                    Post.objects.filter(pk=pk).update(**{'author':post.author,
                                                         'postType':post.postType,
                                                         'create_time':post.create_time,
                                                         'title':form.cleaned_data['title'],
                                                         'content':form.cleaned_data['content']})
                    state='Изменения успешно сохранены.'
            except TypeError:
                state = 'Возникла ошибка! Возможно причина в превышении лимита названия поста, попавшего в БД не через форму'
            return render(request, 'flatpages/messages.html', {'state':state})
        return render(request, 'flatpages/edit.html', {'form':form, 'button':'Сохранить изменения', 'is_author':is_author})
    return render(request,'403.html',{'not_your_publication':True})


@login_required
@permission_required('news_portal.delete_post', raise_exception=True)
def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    if post.author.user == request.user:
        if request.method=='POST':
            post.delete()
            return render(request, 'flatpages/messages.html', {'state': 'Пост успешно удален'})
        return render(request, 'flatpages/del_post.html',{'post':post})
    return render(request, '403.html', {'not_your_publication': True})

class MailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'flatpages/mail/mail.html', {})

    def post(self, request, *args, **kwargs):
        user_2=User.objects.get(pk=62)
        post=Post.objects.get(pk=request.POST.get('post'))
        message=(f'Здравствуй, { request.user.username }!\n'
        f'Рады сообщить, о выходе новой публикации с названием "{ post.title }".\n'
        f'Новая публикация в твоём любимом разделе!\n'
        f'Краткая выдержка:\n'
        f'{ post.content[:151] }...') # шаблон сообщения, сохраняемый в БД модели Mail после отправки
        mail = Mail(subscriber=request.user,
                    message=message,
                    date=request.POST.get('date'))
        html_message = render_to_string('flatpages/mail/send_html_mail.html', {'post':post, 'username':request.user.username})
        email_message = EmailMultiAlternatives(subject=f'{post.title}',body=message,
                                               to=['said-bah@yandex.ru','rfa-kstu@yandex.ru','movchanahsmk@gmail.com']
                                               )
        email_message.attach_alternative(html_message,'text/html')
        email_message.send()
        mail.save()
        return redirect('news_mail')



# представление для тестирования разных задач
def test(request):
    delta=datetime.now(dt.timezone.utc)-dt.timedelta(days=1)
    posts=Post.objects.filter(create_time__gte=delta).count()
    return render(request,'test.html',
                              {'test':posts})

# -! Неиспользуемые классы ниже
class CommListView(ListView):  # класс для отобрпажения
    model = Comment
    template_name = 'flatpages/comm.html'
    context_object_name = 'cmts'