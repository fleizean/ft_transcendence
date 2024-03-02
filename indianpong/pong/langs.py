def get_langs(lang):
    if lang == "en":
        return get_lang_en()
    if lang == "hi":
        return get_lang_hi()
    if lang == "tr":
        return get_lang_tr()
    if lang == "pt":
        return get_lang_pt()


def get_lang_en():
    context = {
        #index
        "baseHeaderText": "Indian-Pong",
        "baseSubHeaderText": "Indian-Pong created for 42 school by Indian Dev!",
        "basePlayButtonText": "Get Started!",

        #Login
        "loginHeaderText1": "Welcome,",
        "loginHeaderText2": "sign in to continue",
        "loginInputUsernameText": "Username",
        "loginInputPasswordText": "Password",
        "loginForgotPasswordText": "Forgot Password?",
        "loginButtonLogin": "Let's go",
        "loginButtonJoin": "Join Us",
        
        #Signup
        "signupHeaderText1": "Welcome,",
        "signupHeaderText2": "sign up to continue",
        "signupInputUsernameText": "Username",
        "signupInputDisplayNameText": "Display Name",
        "signupInputEmailText": "Email",
        "signupInputPasswordText": "Password",
        "signupInputConfirmPasswordText": "Password (again)",
        "signupImageUploadText": "Upload Image",
        "signupButtonSignup": "Let's shine!",


        #Dashboard
        "dashboardText1": "Welcome, ",
        "dashboardText2": "Indian Pong is a collaborative project developed for the 42 school community, offering a nostalgic gaming experience through the classic Atari game, Ping-Pong. This platform allows users to engage in Ping-Pong matches with each other, fostering a sense of friendly competition. In addition to the gaming aspect, Indian Pong provides a social dimension, featuring chat rooms where users can communicate and connect with one another. The platform also enables users to expand their network by adding friends within the 42 school community. Overall, Indian Pong combines the joy of retro gaming with modern social interaction, creating a vibrant and interactive experience for the 42 school community.",

        "dashboardGamesPlayed": "Games Played",
        "dashboardWinCount": "Win Count",
        "dashboardWinStreak": "Win Streak",
        "dashboardLoseStreak": "LoseStreak",
        "dashboardWinRate": "Win Rate",
        "dashboardAverageGameDuration": "Average Game Duration",
        "dashboardAveragePointsWon": "Average Points Won",
        "dashboardAveragePointsLost": "Average Points Lost",

        
        #Pong-Game
        "pongGameHeaderText": "Welcome to Pong Lobby",
        "pongGameSubHeaderText": "You can play with the AI and improve yourself without reflecting it in your stats, as if you were just warming up. If you want to play with a real person, consider the other option, remember that if we don't find someone to match you within 5 minutes, the match will be canceled. Good luck before I forget!",
        "pongGameAIButtonText": "Play with AI",
        "pongGameLocalButtonText": "Local Game",
        "pongGameTournamentButtonText": "Tournament",

            #Local-Game
            "localGameHeaderText": "1v1 Local Game",
            "localGamePlayer1Text": "Player1 Name",
            "localGamePlayer2Text": "Player2 Name",
            "localGameMaxScoreText": "Max Score",
            "localGameGameModeText": "Game Mode",
            "localGameChooseModeText1": "Vanilla",
            "localGameChooseModeText2": "Abilities",
            "localGameButtonStart": "Start",

            #Tournament
            "tournamentHeaderText": "Welcome to Tournament Lobby for Pong",
            "tournamentSubHeaderText": "Here you can join a tournament lobby or create your own tournament lobby. You can invite your friends by sharing the invite code after creating the room. Good luck before I forget!",
            "tournamentJoinButtonText": "Join Tournament",
            "tournamentCreateButtonText": "Create Tournament",

            #Tournament-Create
            "tournamentCreateHeaderText": "CREATE TOURNAMENT",
            "tournamentCreateSubHeaderText": "To create a tournament I need a tournament name, how many max points each game will have. Good luck before I forget!",
            "tournamentCreateNameText": "Tournament Name",
            "tournamentCreateMaxPointsText": "Max Score Games",
            "tournamentCreateGameModeText": "Game Mode",
            "tournamentCreateChooseModeText1": "Vanilla",
            "tournamentCreateChooseModeText2": "Abilities",
            "tournamentCreateButtonCreate": "Create Tournament",

            #Joined-Tournament-Room
            "tournamentroomHeaderText": "Tournament Room",
            "tournamentroomLeaveButtonText": "LEAVE ROOM",
            "tournamentroomStartButtonText": "START ROOM",
            "tournamentCheckBracketButtonText": "CHECK BRACKET",

        #RPS Game
        "rpsGameText1": "Welcome to RPS Lobby",
        "rpsGameText2": "You can play with the AI and improve yourself without reflecting it in your stats, as if you were just warming up. If you want to play with a real person, consider the other option, remember that if we don't find someone to match you within 5 minutes, the match will be canceled. Good luck before I forget!",
        "rpsGameAIButtonText": "Play with AI",
        "rpsGameLocalButtonText": "Local Game",
        "rpsGameSearchOpponentButtonText": "Search Opponent ",

        #Rankings
        "rankingsTableRankText": "Rank",
        "rankingsTableNameText": "Name",
        "rankingsTableUsernameText": "Username",
        "rankingsTableWinsText": "Wins",
        "rankingsTableLossesText": "Losses",
        "rankingsTableWinRateText": "Win Rate",
        "rankingsTablePongPointsText": "Pong Points",

        #Store
        "storeText": "Store",
        "storeTagText": "All",
        "storeWalletText": "Wallet",
        "storeWalleinfoText1": "Oyun oynayarak ",
        "storeWalleinfoText2": " kazanabilirsin.",

        #Inventory
        "inventoryText": "Inventory",
        "inventoryTagText": "All",
        "inventoryWalletText": "Wallet",
        "inventoryWalleinfoText1": "Oyun oynayarak ",
        "inventoryWalleinfoText2": " kazanabilirsin.",
        
        #Search
        "searchInputText": "Email or Username or Displayname Search...",
        "searchMessageButtonText": "Message",
        "searchFollowButtonText": "Follow",
        "searchFollowingButtonText": "Following",
        "searchNoResultFoundText": "No result found.",
        
        #Profile
        "profileRankAIText": "I'M JUST ROBOT",
        "profileRankUserText1": " IN RANKINGS",
        "profileRankUserText2": " NO RANKING",
        "profileFollowButton": "Follow",
        "profileFollowingButton": "Following",
        "profileTitleText1": "42 Kocaeli Student",
        "profileTitleText2": "Software Developer",

        "profileMatchHistoryText1": "Opponent",
        "profileMatchHistoryText2": "Result",
        "profileMatchHistoryText3": "Score",
        "profileMatchHistoryText4": "Duration",

        "profileRankText1": "Rank",

        "profileGameStats1": "Games Played:",
        "profileGameStats2": "Loses:",
        "profileGameStats3": "Win Rate:",
        "profileGameStats4": "Win Streak:",
        "profileGameStats5": "Lose Streak:",
        "profileGameStats6": "Average Game Duration:",
        
        #Friends
        "friendsMessageButtonText": "Message",
        "friendsNoResultFoundText": "No result found.",
        
        #ProfileSettings
        "profileSettingsNavbar1": "Edit Profile",
        "profileSettingsNavbar2": "Change Password",
        "profileSettingsNavbar3": "Add Socials",
        "profileSettingsNavbar4": "Blocked Users",
        "profileSettingsNavbar5": "Close Account",

            #Edit-Profile
            "editProfileChangeImageText": "Change Image",
            "editProfileUsernameText": "Username (how your name will appear to other users on the site)",
            "editProfileEmailText": "Email",
            "editProfile42EmailText": "Since you are logged in with 42, your email setting feature is disabled.",
            "editProfileDisplayNameText": "Display Name",
            "editProfileSaveButtonText": "Save Changes",
            
            #Change-Passwordg
            "changePasswordCurrentPasswordText": "Current Password",
            "changePasswordNewPasswordText": "New Password",
            "changePasswordNewConfirmPasswordText": "Confirm New Password",
            "changePasswordSaveButtonText": "Save Password",
            
            #Add-Socials
            "addSocialsLinkedinInputText": "Enter your LinkedIn username",
            "addSocialsTwitterInputText": "Enter your Twitter username",
            "addSocialsGithubInputText": "Enter your Github username",
            "addSocialsIntraInputText": "Enter your 42 Intra username",
            "addSocialsSaveButtonText": "Save Socials",

            #Blocked-Users
            "blockedUsersHeaderText": "Blocked Accounts",
            "blockedUsersSubHeaderText": "You can unblock the accounts you have blocked here.",

            #Close-Account
            "closeAccountHeaderText": "Close Account",
            "closeAccountSubHeaderText": "You can delete your account here. This action is irreversible.",
            "closeAccountButton": "Close Account",
            

    }
    return context

def get_lang_tr():
    context = {
        #index
        "baseHeaderText": "Indian-Pong",
        "baseSubHeaderText": "Indian-Pong Hintli gelistiriciler tarafindan 42 okulu icin gelistirildi!",
        "basePlayButtonText": "Baslayin!",

        #Login
        "loginHeaderText1": "Hos geldiniz,",
        "loginHeaderText2": "devam etmek icin giris yapin",
        "loginInputUsernameText": "Kullanici Adi",
        "loginInputPasswordText": "Sifre",
        "loginForgotPasswordText": "Sifremi Unuttum?",
        "loginButtonLogin": "Giris Yap",
        "loginButtonJoin": "Uye Ol",
        
        #Signup
        "signupHeaderText1": "Hos geldiniz,",
        "signupHeaderText2": "devam etmek icin kaydolun",
        "signupInputUsernameText": "Kullanici Adi",
        "signupInputDisplayNameText": "Gorunen Ad",
        "signupInputEmailText": "E-posta",
        "signupInputPasswordText": "Sifre",
        "signupInputConfirmPasswordText": "Sifreyi Onayla",
        "signupImageUploadText": "Resim Yukle",
        "signupButtonSignup": "Parlayalim!",


        #Dashboard
        "dashboardText1": "Hos geldiniz, ",
        "dashboardText2": "Indian Pong, 42 okulu toplulugu icin gelistirilmis bir isbirligi projesidir ve klasik Atari oyunu Ping-Pong ile nostaljik bir oyun deneyimi sunar. Bu platform, kullanicilarin birbirleriyle Ping-Pong maclari yapmalarina olanak tanir ve dostane rekabet ortami olusturur. Oyun deneyimi disinda, Indian Pong, kullanicilarin birbirleriyle iletisim kurabilecegi ve baglanti kurabilecegi sohbet odalarini iceren bir sosyal boyut sunar. Platform ayrica, kullanicilarin 42 okulu toplulugunda arkadas ekleyerek aglarini genisletmelerine olanak tanir. Genel olarak, Indian Pong, retro oyun keyfini modern sosyal etkilesimle birlestirerek, 42 okulu toplulugu icin canli ve etkilesimli bir deneyim sunar.",

        "dashboardGamesPlayed": "Oynanan Oyunlar",
        "dashboardWinCount": "Kazanma Sayisi",
        "dashboardWinStreak": "Kazanma Serisi",
        "dashboardLoseStreak": "Kaybetme Serisi",
        "dashboardWinRate": "Kazanma Orani",
        "dashboardAverageGameDuration": "Ortalama Oyun Suresi",
        "dashboardAveragePointsWon": "Ortalama Kazanilan Puanlar",
        "dashboardAveragePointsLost": "Ortalama Kaybedilen Puanlar",

        
        #Pong-Game
        "pongGameHeaderText": "Pong Lobisine Hos Geldiniz",
        "pongGameSubHeaderText": "Yapay Zeka ile oynayarak kendinizi gelistirebilir ve istatistiklerinize yansitmadan isinma gibi davranabilirsiniz. Gercek bir kisiyle oynamak istiyorsaniz, diger secenegi dusunun; 5 dakika icinde eslesecek birini bulamazsak, eslesme iptal edilecektir. Unutmadan once iyi sanslar!",
        "pongGameAIButtonText": "Yapay Zeka ile Oyna",
        "pongGameLocalButtonText": "Yerel Oyun",
        "pongGameTournamentButtonText": "Turnuva",

            #Local-Game
            "localGameHeaderText": "1v1 Yerel Oyun",
            "localGamePlayer1Text": "1. Oyuncu Adi",
            "localGamePlayer2Text": "2. Oyuncu Adi",
            "localGameMaxScoreText": "Maksimum Skor",
            "localGameGameModeText": "Oyun Modu",
            "localGameChooseModeText1": "Klasik",
            "localGameChooseModeText2": "Yetenekler",
            "localGameButtonStart": "Basla",

            #Tournament
            "tournamentHeaderText": "Pong icin Turnuva Lobisine Hos Geldiniz",
            "tournamentSubHeaderText": "Burada bir turnuva lobisine katilabilir veya kendi turnuva lobinizi olusturabilirsiniz. Odanizi olusturduktan sonra davet kodunu paylasarak arkadaslarinizi davet edebilirsiniz. Unutmadan once iyi sanslar!",
            "tournamentJoinButtonText": "Turnuvaya Katil",
            "tournamentCreateButtonText": "Turnuva Olustur",

            #Tournament-Create
            "tournamentCreateHeaderText": "TURNUVA OLUSTUR",
            "tournamentCreateSubHeaderText": "Bir turnuva olusturmak icin bir turnuva adina ve her oyunun maksimum kac puan alacagina ihtiyacim var. Unutmadan once iyi sanslar!",
            "tournamentCreateNameText": "Turnuva Adi",
            "tournamentCreateMaxPointsText": "Oyun Basina Maksimum Skor",
            "tournamentCreateGameModeText": "Oyun Modu",
            "tournamentCreateChooseModeText1": "Klasik",
            "tournamentCreateChooseModeText2": "Yetenekler",
            "tournamentCreateButtonCreate": "Turnuva Olustur",

            #Joined-Tournament-Room
            "tournamentroomHeaderText": "Turnuva Odasi",
            "tournamentroomLeaveButtonText": "ODADAN AYRIL",
            "tournamentroomStartButtonText": "ODAYI BASLAT",
            "tournamentCheckBracketButtonText": "ESLESMEYE BAK",

        #RPS Game
        "rpsGameText1": "Tas Kagit Makas Lobisine Hos Geldiniz",
        "rpsGameText2": "Yapay Zeka ile oynayarak kendinizi gelistirebilir ve istatistiklerinize yansitmadan isinma gibi davranabilirsiniz. Gercek bir kisiyle oynamak istiyorsaniz, diger secenegi dusunun; 5 dakika icinde eslesecek birini bulamazsak, eslesme iptal edilecektir. Unutmadan once iyi sanslar!",
        "rpsGameAIButtonText": "Yapay Zeka ile Oyna",
        "rpsGameLocalButtonText": "Yerel Oyun",
        "rpsGameSearchOpponentButtonText": "Rakip Arayin ",

        #Rankings
        "rankingsTableRankText": "Sira",
        "rankingsTableNameText": "Ad",
        "rankingsTableUsernameText": "Kullanici Adi",
        "rankingsTableWinsText": "Kazanmalar",
        "rankingsTableLossesText": "Kayiplar",
        "rankingsTableWinRateText": "Kazanma Orani",
        "rankingsTablePongPointsText": "Pong Puanlari",

        #Store
        "storeText": "Magaza",
        "storeTagText": "Tumu",
        "storeWalletText": "Cuzdan",
        "storeWalleinfoText1": "Oyun oynayarak ",
        "storeWalleinfoText2": " kazanabilirsin.",

        #Inventory
        "inventoryText": "Envanter",
        "inventoryTagText": "Tumu",
        "inventoryWalletText": "Cuzdan",
        "inventoryWalleinfoText1": "Oyun oynayarak ",
        "inventoryWalleinfoText2": " kazanabilirsin.",
        
        #Search
        "searchInputText": "E-posta veya Kullanici Adi veya Gorunen Ad Ara...",
        "searchMessageButtonText": "Mesaj",
        "searchFollowButtonText": "Takip Et",
        "searchFollowingButtonText": "Takip Ediliyor",
        "searchNoResultFoundText": "Sonuc bulunamadi.",
        
        #Profile
        "profileRankAIText": "SADECE ROBOTUM",
        "profileRankUserText1": " SIRALAMADA",
        "profileRankUserText2": " SIRALAMA YOK",
        "profileFollowButton": "Takip Et",
        "profileFollowingButton": "Takip Ediliyor",
        "profileTitleText1": "42 Kocaeli ogrencisi",
        "profileTitleText2": "Yazilim Gelistirici",

        "profileMatchHistoryText1": "Rakip",
        "profileMatchHistoryText2": "Sonuc",
        "profileMatchHistoryText3": "Skor",
        "profileMatchHistoryText4": "Sure",

        "profileRankText1": "Sira",

        "profileGameStats1": "Oynanan Oyunlar:",
        "profileGameStats2": "Kayiplar:",
        "profileGameStats3": "Kazanma Orani:",
        "profileGameStats4": "Kazanma Serisi:",
        "profileGameStats5": "Kaybetme Serisi:",
        "profileGameStats6": "Ortalama Oyun Suresi:",
        
        #Friends
        "friendsMessageButtonText": "Mesaj",
        "friendsNoResultFoundText": "Sonuc bulunamadi.",
        
        #ProfileSettings
        "profileSettingsNavbar1": "Profili Duzenle",
        "profileSettingsNavbar2": "Sifre Degistir",
        "profileSettingsNavbar3": "Sosyal Medya Ekle",
        "profileSettingsNavbar4": "Engellenen Kullanicilar",
        "profileSettingsNavbar5": "Hesabi Kapat",

            #Edit-Profile
            "editProfileChangeImageText": "Resmi Degistir",
            "editProfileUsernameText": "Kullanici Adi (sitenin diger kullanicilari tarafindan nasil gorunecegi)",
            "editProfileEmailText": "E-posta",
            "editProfile42EmailText": "42 ile oturum actiginiz icin e-posta ayarlama ozelligi devre disi birakilmistir.",
            "editProfileDisplayNameText": "Gorunen Ad",
            "editProfileSaveButtonText": "Degisiklikleri Kaydet",
            
            #Change-Passwordg
            "changePasswordCurrentPasswordText": "Mevcut Sifre",
            "changePasswordNewPasswordText": "Yeni Sifre",
            "changePasswordNewConfirmPasswordText": "Yeni Sifreyi Onayla",
            "changePasswordSaveButtonText": "Sifreyi Kaydet",
            
            #Add-Socials
            "addSocialsLinkedinInputText": "LinkedIn kullanici adinizi girin",
            "addSocialsTwitterInputText": "Twitter kullanici adinizi girin",
            "addSocialsGithubInputText": "Github kullanici adinizi girin",
            "addSocialsIntraInputText": "42 Intra kullanici adinizi girin",
            "addSocialsSaveButtonText": "Sosyal Medyalari Kaydet",

            #Blocked-Users
            "blockedUsersHeaderText": "Engellenen Hesaplar",
            "blockedUsersSubHeaderText": "Burada engellediginiz hesaplari acabilirsiniz.",

            #Close-Account
            "closeAccountHeaderText": "Hesabi Kapat",
            "closeAccountSubHeaderText": "Burada hesabinizi silebilirsiniz. Bu islem geri alinamaz.",
            "closeAccountButton": "Hesabi Kapat",
            

    }
    return context


def get_lang_pt():
    context = {
        #index
        "baseHeaderText": "Indian-Pong",
        "baseSubHeaderText": "A versão indiana do clássico jogo Pong",
        "basePlayButtonText": "Vamos Comecar!",

        #Login
        "loginHeaderText1": "Bem-vindo,",
        "loginHeaderText2": "faca login para continuar",
        "loginInputUsernameText": "Nome de Usuário",
        "loginInputPasswordText": "Senha",
        "loginForgotPasswordText": "Esqueceu a Senha?",
        "loginButtonLogin": "Vamos lá",
        "loginButtonJoin": "Junte-se a Nós",
        
        #Signup
        "signupHeaderText1": "Bem-vindo,",
        "signupHeaderText2": "inscreva-se para continuar",
        "signupInputUsernameText": "Nome de Usuário",
        "signupInputDisplayNameText": "Nome de Exibicão",
        "signupInputEmailText": "E-mail",
        "signupInputPasswordText": "Senha",
        "signupInputConfirmPasswordText": "Senha (novamente)",
        "signupImageUploadText": "Carregar Imagem",
        "signupButtonSignup": "Vamos Brilhar!",


        #Dashboard
        "dashboardText1": "Bem-vindo, ",
        "dashboardText2": "O Indian Pong é um projeto colaborativo desenvolvido para a comunidade da escola 42, oferecendo uma experiência de jogo nostálgica através do clássico jogo Atari, Ping-Pong. Esta plataforma permite que os usuários participem de partidas de Ping-Pong uns com os outros, promovendo uma sensacão de competicão amigável. Além do aspecto de jogo, o Indian Pong oferece uma dimensão social, apresentando salas de bate-papo onde os usuários podem se comunicar e se conectar uns com os outros. A plataforma também permite que os usuários expandam sua rede adicionando amigos dentro da comunidade da escola 42. No geral, o Indian Pong combina a alegria dos jogos retrô com a interacão social moderna, criando uma experiência vibrante e interativa para a comunidade da escola 42.",

        "dashboardGamesPlayed": "Jogos Jogados",
        "dashboardWinCount": "Contagem de Vitórias",
        "dashboardWinStreak": "Sequência de Vitórias",
        "dashboardLoseStreak": "Sequência de Derrotas",
        "dashboardWinRate": "Taxa de Vitória",
        "dashboardAverageGameDuration": "Duracão Média do Jogo",
        "dashboardAveragePointsWon": "Pontos Médios Ganhos",
        "dashboardAveragePointsLost": "Pontos Médios Perdidos",

        
        #Pong-Game
        "pongGameHeaderText": "Bem-vindo ao Lobby de Pong",
        "pongGameSubHeaderText": "Você pode jogar com a IA e se aprimorar sem refletir em suas estatísticas, como se estivesse apenas se aquecendo. Se você quiser jogar com uma pessoa real, considere a outra opcão, lembre-se que se não encontrarmos alguém para combinar com você dentro de 5 minutos, a partida será cancelada. Boa sorte antes que eu esqueca!",
        "pongGameAIButtonText": "Jogar com a IA",
        "pongGameLocalButtonText": "Jogo Local",
        "pongGameTournamentButtonText": "Torneio",

            #Local-Game
            "localGameHeaderText": "Jogo Local 1v1",
            "localGamePlayer1Text": "Nome do Jogador 1",
            "localGamePlayer2Text": "Nome do Jogador 2",
            "localGameMaxScoreText": "Pontuacão Máxima",
            "localGameGameModeText": "Modo de Jogo",
            "localGameChooseModeText1": "Vanilla",
            "localGameChooseModeText2": "Habilidades",
            "localGameButtonStart": "Iniciar",

            #Tournament
            "tournamentHeaderText": "Bem-vindo ao Lobby do Torneio de Pong",
            "tournamentSubHeaderText": "Aqui você pode entrar em um lobby de torneio ou criar seu próprio lobby de torneio. Você pode convidar seus amigos compartilhando o código de convite após criar a sala. Boa sorte antes que eu esqueca!",
            "tournamentJoinButtonText": "Entrar no Torneio",
            "tournamentCreateButtonText": "Criar Torneio",

            #Tournament-Create
            "tournamentCreateHeaderText": "CRIAR TORNEIO",
            "tournamentCreateSubHeaderText": "Para criar um torneio, eu preciso de um nome de torneio, quantos pontos máximos cada jogo terá. Boa sorte antes que eu esqueca!",
            "tournamentCreateNameText": "Nome do Torneio",
            "tournamentCreateMaxPointsText": "Pontuacão Máxima dos Jogos",
            "tournamentCreateGameModeText": "Modo de Jogo",
            "tournamentCreateChooseModeText1": "Vanilla",
            "tournamentCreateChooseModeText2": "Habilidades",
            "tournamentCreateButtonCreate": "Criar Torneio",

            #Joined-Tournament-Room
            "tournamentroomHeaderText": "Sala de Torneio",
            "tournamentroomLeaveButtonText": "SAIR DA SALA",
            "tournamentroomStartButtonText": "INICIAR SALA",
            "tournamentCheckBracketButtonText": "VER SUPORTE",

        #RPS Game
        "rpsGameText1": "Bem-vindo ao Lobby de Pedra, Papel e Tesoura",
        "rpsGameText2": "Você pode jogar com a IA e se aprimorar sem refletir em suas estatísticas, como se estivesse apenas se aquecendo. Se você quiser jogar com uma pessoa real, considere a outra opcão, lembre-se que se não encontrarmos alguém para combinar com você dentro de 5 minutos, a partida será cancelada. Boa sorte antes que eu esqueca!",
        "rpsGameAIButtonText": "Jogar com a IA",
        "rpsGameLocalButtonText": "Jogo Local",
        "rpsGameSearchOpponentButtonText": "Buscar Oponente ",

        #Rankings
        "rankingsTableRankText": "Classificacão",
        "rankingsTableNameText": "Nome",
        "rankingsTableUsernameText": "Nome de Usuário",
        "rankingsTableWinsText": "Vitórias",
        "rankingsTableLossesText": "Derrotas",
        "rankingsTableWinRateText": "Taxa de Vitória",
        "rankingsTablePongPointsText": "Pontos Pong",

        #Store
        "storeText": "Loja",
        "storeTagText": "Tudo",
        "storeWalletText": "Carteira",
        "storeWalleinfoText1": "Você pode ganhar ",
        "storeWalleinfoText2": " jogando.",

        #Inventory
        "inventoryText": "Inventário",
        "inventoryTagText": "Tudo",
        "inventoryWalletText": "Carteira",
        "inventoryWalleinfoText1": "Você pode ganhar ",
        "inventoryWalleinfoText2": " jogando.",
        
        #Search
        "searchInputText": "Procurar por e-mail, nome de usuário ou nome de exibicão...",
        "searchMessageButtonText": "Mensagem",
        "searchFollowButtonText": "Seguir",
        "searchFollowingButtonText": "Seguindo",
        "searchNoResultFoundText": "Nenhum resultado encontrado.",
        
        #Profile
        "profileRankAIText": "Eu sou apenas um robô",
        "profileRankUserText1": "Classificado em ",
        "profileRankUserText2": " Nenhuma classificacão ainda",
        "profileFollowButton": "Seguir",
        "profileFollowingButton": "Seguindo",
        "profileTitleText1": "Comunidade 42, "
    }
    return context

def get_lang_hi():
    context = {
        #index
        "baseHeaderText": "इंडियन-पॉन्ग",
        "baseSubHeaderText": "प्रसिद्ध खेल पॉन्ग का भारतीय संस्करण",
        "basePlayButtonText": "शुरू करें!",

        #Login
        "loginHeaderText1": "स्वागत है,",
        "loginHeaderText2": "जारी रखने के लिए साइन इन करें",
        "loginInputUsernameText": "उपयोगकर्ता नाम",
        "loginInputPasswordText": "पासवर्ड",
        "loginForgotPasswordText": "पासवर्ड भूल गए?",
        "loginButtonLogin": "चलो चलते हैं",
        "loginButtonJoin": "हमारे साथ शामिल हों",
        
        #Signup
        "signupHeaderText1": "स्वागत है,",
        "signupHeaderText2": "जारी रखने के लिए साइन अप करें",
        "signupInputUsernameText": "उपयोगकर्ता नाम",
        "signupInputDisplayNameText": "डिस्प्ले नाम",
        "signupInputEmailText": "ईमेल",
        "signupInputPasswordText": "पासवर्ड",
        "signupInputConfirmPasswordText": "पासवर्ड (फिर से)",
        "signupImageUploadText": "छवि अपलोड करें",
        "signupButtonSignup": "चमकाओ!",


        #Dashboard
        "dashboardText1": "स्वागत, ",
        "dashboardText2": "इंडियन पॉन्ग एक सहयोगी परियोजना है जो 42 स्कूल समुदाय के लिए विकसित की गई है, जो शास्त्रीय खेल पिंग-पोंग के माध्यम से नोस्टाल्जिक गेमिंग अनुभव प्रदान करता है। यह प्लेटफ़ॉर्म प्रतिद्वंद्वियों के साथ पिंग-पोंग मैच खेलने की अनुमति देता है, जो एक दूसरे के साथ दोस्ताना प्रतिस्पर्धा का मूल्यांकन करता है। खेल के पहले पहल में, इंडियन पॉन्ग को सामाजिक आयाम प्रदान करता है, जिसमें उपयोगकर्ताओं को एक-दूसरे के साथ संवाद करने और जुड़ने का अवसर प्रदान किया जाता है। प्लेटफ़ॉर्म उपयोगकर्ताओं को 42 स्कूल समुदाय के भीतर दोस्तों को जोड़ने की सुविधा भी प्रदान करता है। समग्र रूप में, इंडियन पॉन्ग पुराने गेमिंग का आनंद और आधुनिक सामाजिक आक्रोश जोड़ते हैं, 42 स्कूल समुदाय के लिए एक जीवंत और अंतर्क्रियात्मक अनुभव बनाते हैं।",

        "dashboardGamesPlayed": "खेल खेले गए",
        "dashboardWinCount": "जीत की गई बार",
        "dashboardWinStreak": "जीत की रेकार्ड",
        "dashboardLoseStreak": "हार की रेकार्ड",
        "dashboardWinRate": "जीतने की दर",
        "dashboardAverageGameDuration": "औसत खेल की अवधि",
        "dashboardAveragePointsWon": "औसत अंक जीते",
        "dashboardAveragePointsLost": "औसत अंक हारे",

        
        #Pong-Game
        "pongGameHeaderText": "पॉन्ग लॉबी में आपका स्वागत है",
        "pongGameSubHeaderText": "आप ए.आई. के साथ खेल सकते हैं और खुद को सुधार सकते हैं बिना अपने स्टैट्स में इसे प्रकट करने के, जैसे कि आप बस गरम कर रहे थे। यदि आप किसी वास्तविक व्यक्ति के साथ खेलना चाहते हैं, तो दूसरा विकल्प विचार करें, याद रखें कि अगर हमे 5 मिनट के भीतर आपको बंधक मिलाने वाला व्यक्ति नहीं मिलता है, तो मैच रद्द कर दिया जाएगा। भूलने से पहले शुभकामनाएं!",
        "pongGameAIButtonText": "ए.आई. के साथ खेलें",
        "pongGameLocalButtonText": "स्थानीय खेल",
        "pongGameTournamentButtonText": "टूर्नामेंट",

            #Local-Game
            "localGameHeaderText": "1v1 स्थानीय खेल",
            "localGamePlayer1Text": "प्लेयर1 नाम",
            "localGamePlayer2Text": "प्लेयर2 नाम",
            "localGameMaxScoreText": "अधिकतम स्कोर",
            "localGameGameModeText": "खेल मोड",
            "localGameChooseModeText1": "वनिला",
            "localGameChooseModeText2": "क्षमताएँ",
            "localGameButtonStart": "प्रारंभ करें",

            #Tournament
            "tournamentHeaderText": "पॉन्ग के टूर्नामेंट लॉबी में आपका स्वागत है",
            "tournamentSubHeaderText": "यहां आप एक टूर्नामेंट लॉबी में शामिल हो सकते हैं या अपनी खुद की टूर्नामेंट लॉबी बना सकते हैं। आप अपने दोस्तों को रुम बनाने के बाद इनवाइट कोड साझा करके इन्वाइट कर सकते हैं। भूलने से पहले शुभकामनाएं!",
            "tournamentJoinButtonText": "टूर्नामेंट में शामिल हों",
            "tournamentCreateButtonText": "टूर्नामेंट बनाएं",

            #Tournament-Create
            "tournamentCreateHeaderText": "टूर्नामेंट बनाएं",
            "tournamentCreateSubHeaderText": "एक टूर्नामेंट बनाने के लिए मुझे एक टूर्नामेंट का नाम, हर खेल के लिए कितना अधिकतम स्कोर होगा। भूलने से पहले शुभकामनाएं!",
            "tournamentCreateNameText": "टूर्नामेंट का नाम",
            "tournamentCreateMaxPointsText": "अधिकतम स्कोर खेलें",
            "tournamentCreateGameModeText": "खेल मोड",
            "tournamentCreateChooseModeText1": "वनिला",
            "tournamentCreateChooseModeText2": "क्षमताएँ",
            "tournamentCreateButtonCreate": "टूर्नामेंट बनाएं",

            #Joined-Tournament-Room
            "tournamentroomHeaderText": "टूर्नामेंट रूम",
            "tournamentroomLeaveButtonText": "रूम छोड़ें",
            "tournamentroomStartButtonText": "रूम शुरू करें",
            "tournamentCheckBracketButtonText": "ब्रैकेट देखें",

        #RPS Game
        "rpsGameText1": "रॉक-पेपर-सैंड लॉबी में आपका स्वागत है",
        "rpsGameText2": "आप ए.आई. के साथ खेल सकते हैं और खुद को सुधार सकते हैं बिना अपने स्टैट्स में इसे प्रकट करने के, जैसे कि आप बस गरम कर रहे थे। यदि आप किसी वास्तविक व्यक्ति के साथ खेलना चाहते हैं, तो दूसरा विकल्प विचार करें, याद रखें कि अगर हमे 5 मिनट के भीतर आपको बंधक मिलाने वाला व्यक्ति नहीं मिलता है, तो मैच रद्द कर दिया जाएगा। भूलने से पहले शुभकामनाएं!",
        "rpsGameAIButtonText": "ए.आई. के साथ खेलें",
        "rpsGameLocalButtonText": "स्थानीय खेल",
        "rpsGameSearchOpponentButtonText": "विरोधी खोजें ",

        #Rankings
        "rankingsTableRankText": "रैंक",
        "rankingsTableNameText": "नाम",
        "rankingsTableUsernameText": "उपयोगकर्ता नाम",
        "rankingsTableWinsText": "जीतें",
        "rankingsTableLossesText": "हारें",
        "rankingsTableWinRateText": "जीतने की दर",
        "rankingsTablePongPointsText": "पॉन्ग अंक",

        #Store
        "storeText": "दुकान",
        "storeTagText": "सभी",
        "storeWalletText": "वॉलेट",
        "storeWalleinfoText1": "खेल खेलकर ",
        "storeWalleinfoText2": " जीत सकते हैं।",

        #Inventory
        "inventoryText": "इन्वेंटरी",
        "inventoryTagText": "सभी",
        "inventoryWalletText": "वॉलेट",
        "inventoryWalleinfoText1": "खेल खेलकर ",
        "inventoryWalleinfoText2": " जीत सकते हैं।",
        
        #Search
        "searchInputText": "ईमेल या उपयोगकर्ता नाम या डिस्प्ले नाम खोजें...",
        "searchMessageButtonText": "संदेश",
        "searchFollowButtonText": "फॉलो करें",
        "searchFollowingButtonText": "फॉलोइंग",
        "searchNoResultFoundText": "कोई परिणाम नहीं मिला।",
        
        #Profile
        "profileRankAIText": "मैं बस रोबोट हूं",
        "profileRankUserText1": " में रैंकिंग में",
        "profileRankUserText2": " कोई रैंकिंग नहीं",
        "profileFollowButton": "फॉलो करें",
        "profileFollowingButton": "फॉलोइंग",
        "profileTitleText1": "42 कोकाइली"
    }
    return context