SEASON_PLAN = """
Привет, ChatGpt!
Представь, что ты лучший в мире сценарист детских сказок. Мы будем создать персонализированную развивающую сказку для ребенка  и которая будет развиваться как бесконечный сериал. 

Мы будем писать сказку для:
{sex}
По имени {name}
Возраст:  {age}
Интересы ребенка: {interests}

Сериал будет состоять из сезонов, каждый сезон состоит из 2 эпизодов, каждый эпизод состоит из 5 серий. Каждая серия должна длиться 5 минут чтения (не менее 3000 символов текста)

Сюжет должен быть не только увлекательным и полным приключений, но и включать элементы, способствующие личностному развитию и преодолению возможных детских проблем. Удостоверься, что текст адаптирован под возраст ребенка и его словарному запасу.

Напиши содержание первого сезона в виде плана серий.  Указывая только названия эпизода, серий и содержащийся в ней урок. Начни без вступления и комментариев сразу с содержания. В конце дай краткую аннотацию к этому сезону, где также опиши развивающий эффект. Не используй знаков #.
"""

SEASON_PLAN_PICTURE = "Нарисуй картинку к {season_number} сезону сказки по её краткому плану: \n {tale_plan}"

FIRST_CHAPTER_PROMPT = """
Напиши текст первой серии из сезона {season_number}. Время чтения 5 минут (не менее 3000 символов). В конце серии используй интригу для мотивации к прочтению следующей серии.  
В конце серии используй  интригующий поворот сюжета для мотивации к прочтению следующей серии.
Удостоверься, что текст адаптирован под возраст ребенка и его словарный запас. В тексте не используй прямую речь и знаки, кроме точки и запятой.  Начни с названия серии.
Время чтения 5 минут (не менее 3000 символов)
"""

NEXT_CHAPTER_PROMPT = """
Напиши текст следующей серии в соответствии с планом этого сезона. Время чтения серии 5 минут (не менее 3000 символов).   В конце серии используй  неявный интригующий поворот сюжета для мотивации к прочтению следующей серии.
Удостоверься, что текст адаптирован под возраст ребенка и его словарному запасу. В тексте не используй прямую речь.  Начни с названия серии.
Время чтения 5 минут (не менее 3000 символов)
"""

GET_TALE_NAME_PROMPT = """
Выведи только название этой сказки. Если названия нет, выведи придуманное.
"""
