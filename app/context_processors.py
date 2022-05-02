from .models import Folder, Comment

def nav_cats(request):
    objects = Folder.objects.all()[:10]
    #comments = Comment.objects.all()
    return {'nav_folder': objects}
