from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from .models import Tag, Question, Answer
from .forms import TagForm, QuestionForm, AnswerForm

def index(request):
    questions = Question.objects.order_by('-date_added')
    context = {'questions':questions}
    return render(request, 'index.html',context)

def tags(request):
    tags = Tag.objects.order_by('text')
    context = {'tags': tags}
    return render(request, 'tags.html',context)

def tag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    questions = tag.question_set.order_by('-date_added')
    context = {'tag':tag, 'questions':questions}
    return render(request, 'tag.html', context)

@login_required
def new_tag(request):
    if request.method != 'POST':
        form = TagForm()
    else:
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('quora:tags'))
    context = {'form':form}
    return render(request, 'new_tag.html',context)

def question(request, question_id):
    question = Question.objects.get(id=question_id)
    answers = question.answer_set.order_by('-rating')
    context = {'question':question, 'answers':answers}
    return render(request, 'question.html', context)



@login_required
def new_question(request, tag_id):
    tag = Tag.objects.get(id=tag_id)

    if request.method != 'POST':
        form = QuestionForm()
    else:
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.tag = tag
            new_question.owner = request.user
            new_question.save()
            return HttpResponseRedirect(reverse('quora:tag',args=[tag_id]))
    
    context = {'tag':tag,'form':form}
    return render(request, 'new_question.html', context)

@login_required
def edit_question(request, question_id):
    question = Question.objects.get(id=question_id)
    tag = question.tag
    if question.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = QuestionForm(instance=question)

    else:
        form = QuestionForm(instance=question, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('quora:tag', args=[tag.id]))
    
    context = {'question': question, 'tag':tag, 'form':form}
    return render(request, 'edit_question.html', context)

@login_required
def answer_question(request, question_id):
    question = Question.objects.get(id=question_id)
    tag = question.tag

    if request.method != 'POST':
        form = AnswerForm()

    else:
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.owner = request.user
            new_answer.rating = 1
            new_answer.question = question
            new_answer.save()
            return HttpResponseRedirect(reverse('quora:question',args=[question_id]))

    context = {'question':question, 'form':form, 'tag':tag}
    return render(request, 'answer_question.html', context)

        
