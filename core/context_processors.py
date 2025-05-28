from .models import Notificacao

def badge_notifs(request):
    if request.user.is_authenticated:
        qtd = Notificacao.objects.filter(user=request.user, lida=False).count()
        return {"notif_novas": qtd}
    return {}
