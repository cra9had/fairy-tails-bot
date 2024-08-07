SEASON_PLAN = """
Привет, ChatGpt!
Представь, что ты лучший в мире сценарист детских сказок. Мы будем создать персонализированную развивающую сказку для ребенка  и которая будет развиваться как бесконечный сериал. 

Мы будем писать сказку для:
{sex}
По имени {name}
Возраст:  {age}
Интересы ребенка: {interests}

Сериал будет состоять из сезонов, каждый сезон состоит из 2 эпизодов, каждый эпизод состоит из 5 серий. 
Сюжет должен быть не только увлекательным и полным приключений, но и включать элементы, способствующие комплексному личностному развитию характера ребенка.  Удостоверься, что текст адаптирован под возраст ребенка и его словарному запасу.
Напиши содержание первого сезона в виде плана серий.  Указывая только названия эпизода, серий и содержащийся в ней урок. Начни без вступления и комментариев сразу с содержания.
В конце дай краткую аннотацию: опиши ожидаемый развивающий эффект и укажи так же, что каждая сказка подготавливает к самостоятельному чтению, развивают словарный запас и воображение даже при пассивном прослушивании сказки.
"""

SEASON_PLAN_CONTINUE = "Напиши содержание второго сезона."

SEASON_PLAN_PICTURE = "Нарисуй картинку к этому сезону 512x512 пикселей, картинка не должна быть мрачной. Используй  реалистичный стиль. План: \n {tale_plan}"

FIRST_CHAPTER_PROMPT = """
Напиши текст первой серии из сезона {season_number} не меньше 700 слов.
Обязательно следуй плану сезона и убедись, что текст строго соответствует следующим  пунктам:
1. Сюжет должен быть не только увлекательным и полным приключений, но и включать развивающий аспект из плана этого сезона.
2. Обеспечь, чтобы развивающий аспект был включен в сюжет неявно, а естественно отражался в сюжете серии.
3. Удостоверься, что текст адаптирован под возраст ребенка и его словарному запасу, а также написан грамотным русским языком.
4. В тексте не используй прямую речь ни в каком виде.
5. Обеспечить, чтобы серия заканчивалась моментом, стимулирующим интерес к продолжению.
6. Начни сразу с названия серии, после названия поставь точку.
7. В тексте не используй  знаки тире, дефис "-" и двоеточие ":", а также не используй решетку "#"
8. "Длина текста этой серии должна быть более 700 слов"
"""

NEXT_CHAPTER_PROMPT = """
Напиши текст следующей серии не меньше 700 слов
Обязательно следуй плану сезона и убедись, что текст строго соответствует следующим  пунктам:
1. Сюжет должен быть не только увлекательным и полным приключений, но и включать развивающий аспект из плана этого сезона.
2. Обеспечь, чтобы развивающий аспект был включен в сюжет неявно, а естественно отражался в сюжете серии.
3. Удостоверься, что текст адаптирован под возраст ребенка и его словарному запасу, а также написан грамотным русским языком.
4. В тексте не используй прямую речь ни в каком виде.
5. Обеспечить, чтобы серия заканчивалась моментом, стимулирующим интерес к продолжению.
6. Начни сразу с названия серии, после названия поставь точку.
7. В тексте не используй  знаки тире, дефис "-" и двоеточие ":", а также не используй решетку "#"
8. "Длина текста этой серии должна быть более 700 слов"
"""

GET_TALE_NAME_PROMPT = """
Выведи только название этой сказки. Если названия нет, выведи придуманное.
"""
