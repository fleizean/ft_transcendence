from django import template


register = template.Library()

@register.simple_tag(takes_context=True)
def transnav(context):
    request = context['request']
    lang = request.COOKIES.get('selectedLanguage', 'en')
    d = {'tr': "Ana Sayfa", 'en': "Dashboard", 'hi': "डैशबोर्ड", 'pt': "Página Inicial"}
    c = {'tr': "Sohbet", 'en': "Chat", 'hi': "चैट", 'pt': "Bate-papo"}
    p = {'tr': "Pong Oyunu", 'en': "Pong Game", 'hi': "पोंग खेल", 'pt': "Jogo de Pong"}
    t = {'tr': "TKM Oyunu", 'en': "RPS Game", 'hi': "पत्थर-कागज-कैंची", 'pt': "PPT Jogo"}
    r = {'tr': "Sıralama", 'en': "Ranking", 'hi': "रैंकिंग", 'pt': "Classificação"}
    s = {'tr': "Mağaza", 'en': "Store", 'hi': "स्टोर", 'pt': "Loja"}
    a = {'tr': "Arama", 'en': "Search", 'hi': "खोज", 'pt': "Pesquisa"}
    h = {'tr': "Hakkımızda", 'en': "About Us", 'hi': "हमारे बारे में", 'pt': "Sobre nós"}
    f = {'tr': "Profil", 'en': "Profile", 'hi': "प्रोफाइल", 'pt': "Perfil"}
    k = {'tr': "Arkadaşlar", 'en': "Friends", 'hi': "मित्र", 'pt': "Amigos"}
    g = {'tr': "Profil Ayarları", 'en': "Profile Settings", 'hi': "प्रोफाइल सेटिंग्स", 'pt': "Configurações do Perfil"}
    o = {'tr': "Çıkış", 'en': "Logout", 'hi': "लॉग आउट", 'pt': "Sair"}
    return d[lang], c[lang], p[lang], t[lang], r[lang], s[lang], a[lang], h[lang], f[lang], k[lang], g[lang], o[lang]
