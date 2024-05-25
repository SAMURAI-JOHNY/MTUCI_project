from lol.models import LolBlocks, UserLol, Lol


def lol_procents(request):
    progress_list = dict()
    courses = Lol.objects.values('course_name')
    for current_course in courses:
        blocks = LolBlocks.objects.filter(course_name=current_course['course_name'])
        user_blocks = UserLol.objects.filter(course_name=current_course['course_name'], user_id=request.user.id, status=1)
        progress = round((user_blocks.count() / blocks.count()) * 100)
        progress_list[current_course['course_name']] = progress
    return progress_list