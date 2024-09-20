from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import decorator_from_middleware
from .models import Questions, FriendAnswers
import random

def no_cache(view_func):
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return wrapper

@no_cache
def game(request):
    curr_level = ['easy','easy','easy','easy','medium','medium','medium','medium','hard','hard','hard','impossible']
    points = [0, 500, 1000, 2000, 5000, 10000, 20000, 40000, 75000, 125000, 250000, 500000, 1000000]
    try:
        if request.method == 'POST':

            #               Check if answer is correct
            question = request.session.get('question')
            curr_question = get_object_or_404(Questions, id=question['id'])
            selected_answer = request.POST.get('answer')
            fifty_fifty = request.POST.get('fifty_fifty')
            friend_call = request.POST.get('friend_call')
            public_opinion = request.POST.get('public_opinion')
            refresh_question = request.POST.get('refresh_question')


            wrong_answer = request.POST.get('back')
            if wrong_answer:
                return home()

            if selected_answer:
                request.session['fifty_fifty_current'] = False
                request.session['friend_call_current'] = False
                request.session['public_opinion_current'] = False
                request.session['buttons_to_hide'] = []

                request.session['prob_answ_a'] = ''
                request.session['prob_answ_b'] = ''
                request.session['prob_answ_c'] = ''
                request.session['prob_answ_d'] = ''
                request.session['message'] = ''


                if selected_answer == question['correct']:
                    message = "Correct!"
                    request.session['new_game'] = False

                    #                  Update session
                    question_number = request.session.get('question_number', 0) + 1

                    if question_number == 13:
                        return redirect('congratulations')

                    request.session['curr_points'] = points[question_number]
                    request.session['question_number'] = question_number
                    answered_questions_list = request.session.get('answered_questions', [])


                    if not isinstance(answered_questions_list, list):
                        answered_questions_list = [answered_questions_list]

                    #                  Get new question (different from previous)

                    quest_db = Questions.objects.filter(level=curr_level[question_number-1]).exclude(id__in=answered_questions_list)
                    quest_count = quest_db.count()
                    random_index = random.randint(0, quest_count - 1)
                    random_record = quest_db[random_index]

                    #                   Safe info to session
                    answered_questions_list.append(random_record.id)
                    request.session['answered_questions'] = answered_questions_list
                    request.session['question'] = {
                        'id': random_record.id,
                        'text': random_record.question,
                        'answer_a': random_record.answer_a,
                        'answer_b': random_record.answer_b,
                        'answer_c': random_record.answer_c,
                        'answer_d': random_record.answer_d,
                        'correct': random_record.correct_answer,
                        'type': random_record.question_type,
                    }
                    context = {
                        'question': request.session.get('question'),
                        'curr_points': request.session.get('curr_points', 0),
                        'question_number': request.session.get('question_number', 0),
                        'fifty_fifty': request.session['fifty_fifty'],
                        'friend_call': request.session['friend_call'],
                        'public_opinion': request.session['public_opinion'],
                        'refresh_question': request.session['refresh_question'],
                        'friend': request.session['friend'],
                    }
                    #return redirect(game)
                    return render(request, "base.html", context)
                else:
                    context = {
                        'question': request.session.get('question'),
                        'curr_points': request.session.get('curr_points', 0),
                        'question_number': request.session.get('question_number', 0),
                        'fifty_fifty': request.session['fifty_fifty'],
                        'friend_call': request.session['friend_call'],
                        'public_opinion': request.session['public_opinion'],
                        'refresh_question': request.session['refresh_question'],
                        'friend': request.session['friend'],
                        'wrong_answer': 'siema',
                    }
                    return render(request, "base.html", context)
            elif fifty_fifty:
                request.session['fifty_fifty'] = True
                request.session['fifty_fifty_current'] = True
                buttons = ['answer_a', 'answer_b', 'answer_c', 'answer_d']
                buttons.remove(question['correct'])
                buttons_to_hide = random.sample(buttons, 2)  # Losowo wybierz dwa przyciski
                request.session['buttons_to_hide'] = buttons_to_hide
                context = {
                    'question': request.session.get('question'),
                    'curr_points': request.session.get('curr_points', 0),
                    'question_number': request.session.get('question_number', 0),
                    'fifty_fifty_used': True,
                    'fifty_fifty': request.session['fifty_fifty'],
                    'friend_call': request.session['friend_call'],
                    'public_opinion': request.session['public_opinion'],
                    'refresh_question': request.session['refresh_question'],
                    'buttons_to_hide': request.session.get('buttons_to_hide', []),
                    'message': request.session.get('message', ''),
                    'friend': request.session['friend'],
                    'prob_answ_a': request.session.get('prob_answ_a', ''),
                    'prob_answ_b': request.session.get('prob_answ_b', ''),
                    'prob_answ_c': request.session.get('prob_answ_c', ''),
                    'prob_answ_d': request.session.get('prob_answ_d', ''),
                }
                return render(request, "base.html", context)
            elif friend_call:
                request.session['friend_call'] = True
                request.session['firend_call_current'] = True
                friend_type = request.session['friend_type'],
                question_number = request.session.get('question_number', 0)

                random_number = random.randint(0, 19)
                correct = False
                idk = False



                answers = ["a", "b", "c", "d"]
                if request.session.get('fifty_fifty_current', False):
                    buttons_to_hide = request.session['buttons_to_hide']
                    if "answer_a" in buttons_to_hide:
                        answers.remove("a")
                    if "answer_b" in buttons_to_hide:
                        answers.remove("b")
                    if "answer_c" in buttons_to_hide:
                        answers.remove("c")
                    if "answer_d" in buttons_to_hide:
                        answers.remove("d")
                if friend_type[0] == curr_question.question_type:
                    if question_number < 9:
                        answ_db = FriendAnswers.objects.filter(answer_type='certain')
                        if random_number < 18:
                            correct = True
                    elif question_number < 12:
                        # 65% for correct answ
                        # 20% for certain
                        if random_number < 4:
                            answ_db = FriendAnswers.objects.filter(answer_type='certain')
                            correct = True
                        elif random_number < 13:
                            answ_db = FriendAnswers.objects.filter(answer_type='not_sure')
                            correct = True
                        else:
                            answ_db = FriendAnswers.objects.filter(answer_type='dont_know')
                            idk=True
                    else:
                        answ_db = FriendAnswers.objects.filter(answer_type='dont_know')
                        idk=True
                else:
                    if question_number < 9:
                        answ_db = FriendAnswers.objects.filter(answer_type='not_sure')
                        if random_number < 8:
                            correct = True
                    elif question_number < 12:
                        # 20% for correct
                        if random_number < 4:
                            answ_db = FriendAnswers.objects.filter(answer_type='not_sure')
                            correct = True
                        elif random_number < 9:
                            answ_db = FriendAnswers.objects.filter(answer_type='not_sure')
                        else:
                            answ_db = FriendAnswers.objects.filter(answer_type='dont_know')
                            idk=True
                    else:
                        answ_db = FriendAnswers.objects.filter(answer_type='dont_know')
                        idk=True

                answ_count = answ_db.count()
                random_index = random.randint(0, answ_count - 1)
                random_answ = answ_db[random_index].answer

                if idk:
                    message = str(random_answ)
                elif correct:
                    message = str(random_answ) + ' ' + str(curr_question.correct_answer[-1])
                else:
                    message = str(random_answ) + ' ' + str(random.choice(answers))


                request.session['message'] = message
                context = {
                    'question': request.session.get('question'),
                    'curr_points': request.session.get('curr_points', 0),
                    'question_number': request.session.get('question_number', 0),
                    'friend_call_used': True,
                    'fifty_fifty': request.session['fifty_fifty'],
                    'friend_call': request.session['friend_call'],
                    'public_opinion': request.session['public_opinion'],
                    'refresh_question': request.session['refresh_question'],
                    'friend': request.session['friend'],
                    'buttons_to_hide': request.session.get('buttons_to_hide', []),
                    'message': request.session.get('message', ''),
                    'prob_answ_a': request.session.get('prob_answ_a', ''),
                    'prob_answ_b': request.session.get('prob_answ_b', ''),
                    'prob_answ_c': request.session.get('prob_answ_c', ''),
                    'prob_answ_d': request.session.get('prob_answ_d', ''),
                }
                return render(request, "base.html", context)
            elif public_opinion:
                request.session['public_opinion'] = True
                request.session['public_opinion_current'] = True
                question_number = request.session.get('question_number', 0)

                prob_boost = 0
                if question_number < 5:
                    prob_boost = 80
                elif question_number < 9:
                    prob_boost = 50
                elif question_number < 12:
                    prob_boost = 20
                else:
                    prob_boost = 0

                buttons_to_hide = request.session.get('buttons_to_hide', 0)

                #if buttons_to_hide checks if its not empty
                if request.session.get('fifty_fifty_current', False) or buttons_to_hide:
                    buttons_to_hide = request.session['buttons_to_hide']
                    buttons = ['answer_a', 'answer_b', 'answer_c', 'answer_d']
                    buttons.remove(buttons_to_hide[0])
                    buttons.remove(buttons_to_hide[1])
                    if "answer_a" in buttons:
                        prob_answ_a = random.randint(10,99)
                        if curr_question.correct_answer == 'answer_a':
                            prob_answ_a += prob_boost
                    else:
                        prob_answ_a = 0
                    if "answer_b" in buttons:
                        prob_answ_b = random.randint(10,99)
                        if curr_question.correct_answer == 'answer_b':
                            prob_answ_b += prob_boost
                    else:
                        prob_answ_b = 0
                    if "answer_c" in buttons:
                        prob_answ_c = random.randint(10,99)
                        if curr_question.correct_answer == 'answer_c':
                            prob_answ_c += prob_boost
                    else:
                        prob_answ_c = 0
                    if "answer_d" in buttons:
                        prob_answ_d = random.randint(10,99)
                        if curr_question.correct_answer == 'answer_d':
                            prob_answ_d += prob_boost
                    else:
                        prob_answ_d = 0
                else:
                    prob_answ_a = random.randint(10,99)
                    prob_answ_b = random.randint(10,99)
                    prob_answ_c = random.randint(10,99)
                    prob_answ_d = random.randint(10,99)

                    if curr_question.correct_answer == 'answer_a':
                        prob_answ_a+=prob_boost
                    elif curr_question.correct_answer == 'answer_b':
                        prob_answ_b+=prob_boost
                    elif curr_question.correct_answer =='answer_c':
                        prob_answ_c+=prob_boost
                    else:
                        prob_answ_d+=prob_boost

                ######
                request.session['prob_answ_a'] = str(round(100*prob_answ_a/(prob_answ_a+prob_answ_b+prob_answ_c+prob_answ_d), 1)) + '%'
                request.session['prob_answ_b'] = str(round(100*prob_answ_b/(prob_answ_a+prob_answ_b+prob_answ_c+prob_answ_d), 1)) + '%'
                request.session['prob_answ_c'] = str(round(100*prob_answ_c/(prob_answ_a+prob_answ_b+prob_answ_c+prob_answ_d), 1)) + '%'
                request.session['prob_answ_d'] = str(round(100*prob_answ_d/(prob_answ_a+prob_answ_b+prob_answ_c+prob_answ_d), 1)) + '%'
                context = {
                    'question': request.session.get('question'),
                    'curr_points': request.session.get('curr_points', 0),
                    'question_number': request.session.get('question_number', 0),
                    'public_opinion_used': True,
                    'fifty_fifty': request.session['fifty_fifty'],
                    'friend_call': request.session['friend_call'],
                    'public_opinion': request.session['public_opinion'],
                    'refresh_question': request.session['refresh_question'],
                    'prob_answ_a': request.session.get('prob_answ_a', ''),
                    'prob_answ_b': request.session.get('prob_answ_b', ''),
                    'prob_answ_c': request.session.get('prob_answ_c', ''),
                    'prob_answ_d': request.session.get('prob_answ_d', ''),
                    'buttons_to_hide': request.session.get('buttons_to_hide', []),
                    'message': request.session.get('message', ''),
                    'friend': request.session['friend'],
                }
                return render(request, "base.html", context)
            elif refresh_question:
                request.session['refresh_question'] = True
                question_number = request.session.get('question_number', 0)
                answered_questions_list = request.session.get('answered_questions', [])

                quest_db = Questions.objects.filter(level=curr_level[question_number - 1]).exclude(id__in=answered_questions_list)
                quest_count = quest_db.count()
                random_index = random.randint(0, quest_count - 1)
                random_record = quest_db[random_index]
                request.session['question_id'] = random_record.id
                answered_questions_list.append(random_record.id)
                request.session['answered_questions'] = answered_questions_list
                request.session['question'] = {
                    'id': random_record.id,
                    'text': random_record.question,
                    'answer_a': random_record.answer_a,
                    'answer_b': random_record.answer_b,
                    'answer_c': random_record.answer_c,
                    'answer_d': random_record.answer_d,
                    'correct': random_record.correct_answer,
                    'type': random_record.question_type,
                }

                context = {
                    'question': request.session.get('question'),
                    'curr_points': request.session.get('curr_points', 0),
                    'question_number': request.session.get('question_number', 0),
                    'refresh_question_used': True,
                    'fifty_fifty': request.session['fifty_fifty'],
                    'friend_call': request.session['friend_call'],
                    'public_opinion': request.session['public_opinion'],
                    'refresh_question': request.session['refresh_question'],
                    'friend': request.session['friend'],
                }
                return render(request, "base.html", context)
    except:
        return redirect('home')
    new_game = request.session.get('new_game', True)
    try:
        if new_game:
            #   This code is executed first time reaching the site
            quest_db = Questions.objects.filter(level='easy')
            quest_count = quest_db.count()
            random_index = random.randint(0, quest_count - 1)
            random_record = quest_db[random_index]

            request.session['question'] = {
                'id': random_record.id,
                'text': random_record.question,
                'answer_a': random_record.answer_a,
                'answer_b': random_record.answer_b,
                'answer_c': random_record.answer_c,
                'answer_d': random_record.answer_d,
                'correct': random_record.correct_answer,
                'type': random_record.question_type,
            }
            request.session['question_id'] = random_record.id
            request.session['question_number'] = 1
            request.session['curr_points'] = points[1]
            request.session['answered_questions'] = [random_record.id,]

            request.session['fifty_fifty'] = False
            request.session['friend_call'] = False
            request.session['public_opinion'] = False
            request.session['refresh_question'] = False

            request.session['new_game'] = False

            context = {
                'question': request.session.get('question'),
                'curr_points': request.session.get('curr_points', 0),
                'question_number': request.session.get('question_number', 0),
                'friend': request.session['friend'],
            }
            return render(request, "base.html", context)
        else:
            context = {
                'question': request.session.get('question'),
                'curr_points': request.session.get('curr_points', 0),
                'question_number': request.session.get('question_number', 0),
                'fifty_fifty': request.session['fifty_fifty'],
                'friend_call': request.session['friend_call'],
                'public_opinion': request.session['public_opinion'],
                'refresh_question': request.session['refresh_question'],
                'friend': request.session['friend'],
                'prob_answ_a': request.session.get('prob_answ_a', ''),
                'prob_answ_b': request.session.get('prob_answ_b', ''),
                'prob_answ_c': request.session.get('prob_answ_c', ''),
                'prob_answ_d': request.session.get('prob_answ_d', ''),
                'buttons_to_hide': request.session.get('buttons_to_hide', []),
                'message': request.session.get('message', ''),
            }
            return render(request, "base.html", context)
    except:
        return redirect('home')



def home(request):
    request.session.flush()
    return render(request, "home.html")

def congratulations(request):
    return render(request, "congratulations.html")

def start_game(request):
    if request.method == "POST":
        request.session.flush()
        request.session['new_game'] = True
        selected_option = request.POST.get('friend')
        request.session['friend'] = selected_option
        if selected_option == 'Rafael':
            request.session['friend_type'] = 'lore'
        elif selected_option == 'Old Player':
            request.session['friend_type'] = 'game'
        elif selected_option == 'John':
            request.session['friend_type'] = 'esport'
        elif selected_option == 'Frek':
            request.session['friend_type'] = 'nothing'

        return redirect('game')
    else:
        return home()
