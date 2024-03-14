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
        "basePageTittle": "Indian-Pong",
        "baseHeaderText": "Indian-Pong",
        "baseSubHeaderText": "Indian-Pong created for 42 school by Indian Dev!",
        "basePlayButtonText": "Get Started!",

        "baseInfoHeaderText": "Welcome to Indian-Pong!",
        "baseInfoHeaderDescription": "Pong brings the excitement and competition of classic table tennis to the internet. On this platform, you can have fun, showcase your skills, and rise in the rankings to become one of the best.",
        "baseInfoSubHeaderText": "Play and Win",
        "baseInfoSubHeaderDescription1": "Gain Pong Points with each game you win to climb the ranks.",
        "baseInfoSubHeaderDescription2": "Use your earnings to purchase new items, rackets, and tables from the store to enhance your gaming experience.",
        "baseInfoSubHeaderText2": "Get Started Now",
        "baseInfoSubHeaderDescription3": "Create an account to personalize your profile, track your statistics, and see where you stand in the rankings.",
        "baseInfoSubHeaderText3": "More Features",
        "baseInfoSubHeaderDescription4": "Participate in tournaments to face off against your opponents.",
        "baseInfoSubHeaderDescription5": "Enjoy quality time with your friends by hosting private games.",
        "baseInfoSubHeaderDescription6": "Chat with other players, share tactics, and join the Pong community.",
        
        #Login
        "loginPageTittle": "Login",
        "loginHeaderText1": "Welcome,",
        "loginHeaderText2": "sign in to continue",
        "loginInputUsernameText": "Username",
        "loginInputPasswordText": "Password",
        "loginForgotPasswordText": "Forgot Password?",
        "loginButtonLogin": "Let's go",
        "loginButtonJoin": "Join Us",

        #404
        "notFoundPageTittle": "404 Not Found",
        "notFoundHeaderText": "404 ERROR",
        "notFoundSubHeaderText": "Probably you lost in our website!",
        
        #Signup
        "signupPageTittle": "Sign Up",
        "signupHeaderText1": "Welcome,",
        "signupHeaderText2": "sign up to continue",
        "signupInputUsernameText": "Username",
        "signupInputDisplayNameText": "Display Name",
        "signupInputEmailText": "Email",
        "signupInputPasswordText": "Password",
        "signupInputConfirmPasswordText": "Password (again)",
        "signupImageUploadText": "Upload Image",
        "signupButtonSignup": "Let's shine!",

        #ForgotPassword
        "forgotPasswordPageTittle": "Forgot Password",
        "forgotPasswordHeaderText": "Forgot Password",
        "forgotPasswordInputEmailText": "Email",
        "forgotPasswordButtonSend": "Send Email",
        "forgotPasswordLinkText": "Don't have an account?",
        "forgotPasswordLinkButtonText": "Join Us",

        #ChangePassword
        "changePasswordPageTittle": "Change Password",
        "changePasswordHeaderText": "Change Password",
        "changePassswordSubHeaderText": "change your password",

        #Dashboard
        "dashboardPageTittle": "Dashboard",
        "dashboardText1": "Welcome, ",
        "dashboardText2": "Indian Pong is a collaborative project developed for the 42 school community, offering a nostalgic gaming experience through the classic Atari game, Ping-Pong. This platform allows users to engage in Ping-Pong matches with each other, fostering a sense of friendly competition. In addition to the gaming aspect, Indian Pong provides a social dimension, featuring chat rooms where users can communicate and connect with one another. The platform also enables users to expand their network by adding friends within the 42 school community. Overall, Indian Pong combines the joy of retro gaming with modern social interaction, creating a vibrant and interactive experience for the 42 school community.",

        "dashboardGamesPlayed": "Games Played",
        "dashboardWinCount": "Win Count",
        "dashboardWinStreak": "Win Streak",
        "dashboardLoseStreak": "Lose Streak",
        "dashboardWinRate": "Win Rate",
        "dashboardAverageGameDuration": "Average Game Duration",
        "dashboardAveragePointsWon": "Average Points Won",
        "dashboardAveragePointsLost": "Average Points Lost",

        
        #Pong-Game
        "pongGamePageTittle": "Pong Game",
        "pongGameHeaderText": "Welcome to Pong Lobby",
        "pongGameSubHeaderText": "You can improve yourself by playing with Artificial Intelligence. If you want to play with a real person, consider the other option; if we don't find someone to match with in 5 minutes, the match will be canceled. Good luck before we forget!",
        "pongGameAIButtonText": "Play with AI",
        "pongGameLocalButtonText": "Local Game",
        "pongGameRemoteButtonText": "Remote Player",
        "pongGameLocalTournamentButtonText": "Local Tournament",
        "pongGameTournamentButtonText": "Tournament",

            #AI-Game
            "aiGamePageTittle": "AI Game",
            "aiGameReactionDelayText": "Reaction Delay",
            "aiGameGetReadyText": "Get Ready",
            "aiGamePresSpaceText": "Press 'Space' to start",
            "aiGameCountdownText": "Starting in",

            "aiGameGameOverText": "Game Over",
            "aiGameRestartButtonText": "Restart",
            "aiGameExitButtonText": "Exit",

            "aiGameInfoHeaderText": "About the Game",
            "aiGameInfoSubHeaderText": "How to Play the Game?",
            "aiGameInfoSubHeaderDescription1": "In Pong game, players engage in a table tennis match against their opponents. The W-A-S-D keys (or up-down-left-right arrow keys) are used to control the ball.",
            "aiGameInfoSubHeaderText2": "Win and Improve",
            "aiGameInfoSubHeaderDescription2": "You earn Pong Points with every game you win. With these points, you can purchase new items, rackets, and tables from the store to enhance your gaming experience.",
            "aiGameInfoSubHeaderText3": "Get Started Now",
            "aiGameInfoSubHeaderDescription3": "You can create an account to personalize your gaming experience. With an account, you can track your statistics and see your position in the rankings.",
            "aiGameInfoSubHeaderText4": "More Features",
            "aiGameInfoSubHeaderDescription4": "You can participate in tournaments to face off against your opponents and test your skills. Additionally, you can create private games with your friends and join the Pong community.",

            "aiGameInfoSubHeaderText5": "Controls",
            "aiGameInfoSubHeaderDescription5": "Up",
            "aiGameInfoSubHeaderDescription6": "Down",
            "aiGameInfoSubHeaderText6": "Skills",
            "aiGameInfoSubHeaderDescription7": "Like a Cheater",
            "aiGameInfoSubHeaderDescription8": "Fast and Furious",
            "aiGameInfoSubHeaderDescription9": "Frozen Ball",

            #Local-Game
            "localGamePageTittle": "Local Game",
            "localGameHeaderText": "1v1 Local Game",
            "localGamePlayer1Text": "Player1 Name",
            "localGamePlayer2Text": "Player2 Name",
            "localGameMaxScoreText": "Max Score",
            "localGameGameModeText": "Game Mode",
            "localGameChooseModeText1": "Vanilla",
            "localGameChooseModeText2": "Abilities",
            "localGameButtonStart": "Start",

            #Local-Tournament
            "localTournamentPageTittle": "Local Tournament",
            "localTournamentGameHeaderText": "Local Tournament",
            "localTournamentPlayer1Text": "Player1 Name",
            "localTournamentPlayer2Text": "Player2 Name",
            "localTournamentPlayer3Text": "Player3 Name",
            "localTournamentPlayer4Text": "Player4 Name",
            "localTournamentMaxScoreText": "Max Score",
            "localTournamentGameModeText": "Game Mode",
            "localTournamentChooseModeText1": "Vanilla",
            "localTournamentChooseModeText2": "Abilities",
            "localTournamentButtonStart": "Start & Bracket",
            "localTournamentBracketTitle": "Tournament Bracket",
            "localTournamentBracketStartButtonText": "Start Tournament",
            "localTournamentTournamentOverText": "Tournament Over",
            "localTournamentOverButtonText": "Over",

            "localTournamentNextButtonText": "Next",


            #Tournament
            "tournamentPageTittle": "Tournament",
            "tournamentHeaderText": "Welcome to Tournament Lobby for Pong",
            "tournamentSubHeaderText": "Here you can join a tournament lobby or create your own tournament lobby. You can invite your friends by sharing the invite code after creating the room. Good luck before I forget!",
            "tournamentJoinButtonText": "Join Tournament",
            "tournamentCreateButtonText": "Create Tournament",

            #Tournament-Create
            "tournamentCreatePageTittle": "Create Tournament",
            "tournamentCreateHeaderText": "CREATE TOURNAMENT",
            "tournamentCreateSubHeaderText": "To create a tournament I need a tournament name, how many max points each game will have. Good luck before I forget!",
            "tournamentCreateNameText": "Tournament Name",
            "tournamentCreateMaxPointsText": "Max Score Games",
            "tournamentCreateGameModeText": "Game Mode",
            "tournamentCreateChooseModeText1": "Vanilla",
            "tournamentCreateChooseModeText2": "Abilities",
            "tournamentCreateButtonCreate": "Create Tournament",

            #Joined-Tournament-Room
            "tournamentroomPageTittle": "Tournament Room",
            "tournamentroomHeaderText": "Tournament Room",
            "tournamentroomRoomText": "Room",
            "tournamentroomLeaveButtonText": "LEAVE TOURNAMENT",
            "tournamentroomStartButtonText": "START TOURNAMENT",
            "tournamentroomJoinButtonText": "JOIN TOURNAMENT",
            "tournamentCheckBracketButtonText": "CHECK BRACKET",
            "tournamentroomTournamentRoomButton": "TOURNAMENT ROOM",
            "tournamentroomWaitingText": "Waiting",
            "tournamentroomForPlayerText": "for player...",

            #Tournament Room List
            "tournamentRoomListPageTittle": "Tournament Rooms",
            "tournamentRoomListHeaderText": "Tournament Rooms",

        #RPS Game
        "rpsGamePageTittle": "Rock Paper Scissors",
        "rpsGameText1": "Welcome to RPS Lobby",
        "rpsGameText2": "You can improve yourself by playing with Artificial Intelligence. If you want to play with a real person, consider the other option; if we don't find someone to match with in 5 minutes, the match will be canceled. Good luck before we forget!",
        "rpsGameAIButtonText": "Play with AI",
        "rpsGameLocalButtonText": "Local Game",
        "rpsGameSearchOpponentButtonText": "Search Opponent ",

        #AI-Game
            "rpsGamePageTittle": "RPS Game with Artificial Intelligence",
            "rpsGameScoreText": "score",
            "rpsGameRockText": "ROCK",
            "rpsGamePaperText": "PAPER",
            "rpsGameScissorsText": "SCISSORS",
            "rpsGamePickedText": "you picked",
            "rpsGamePickedText2": "the house picked",
            "rpsGameAgainText": "Play again",
            "rpsGameGameOverText": "Game Over",
            "rpsGameRestartButtonText": "Restart",
            "rpsGameExitButtonText": "Exit",

        #Rankings
        "rankingsPageTittle": "Rankings",
        "rankingsTableRankText": "Rank",
        "rankingsTableNameText": "Name",
        "rankingsTableUsernameText": "Username",
        "rankingsTableWinsText": "Wins",
        "rankingsTableLossesText": "Losses",
        "rankingsTableWinRateText": "Win Rate",
        "rankingsTablePongPointsText": "Pong Point",

        #Store
        "storePageTittle": "Store",
        "storeText": "Store",
        "storeTagText": "All",
        "storeWalletText": "Wallet",
        "storeWalleinfoText1": "Oyun oynayarak ",
        "storeWalleinfoText2": " kazanabilirsin.",

        #Inventory
        "inventoryPageTittle": "Inventory",
        "inventoryText": "Inventory",
        "inventoryTagText": "All",
        "inventoryWalletText": "Wallet",
        "inventoryWalleinfoText1": " playing games",
        "inventoryWalleinfoText2": " can win.",
        "inventoryModalHeaderText": "Set Featured Item",
        "inventoryModalSaveButton": "Save",
        "inventoryModalCloseButton": "Close",
        "inventoryItemKeyboardInfoText": "Use the",
        "inventoryItemKeyboardInfoText2": "key to use this ability. And remember, you must equip this ability.",
        "inventoryItemKeyboardInfoText3": "There is no special keypad for this item, it is used automatically.",
        
        #Search
        "searchPageTittle": "Search",
        "searchInputText": "Email or Username or Displayname Search...",
        "searchMessageButtonText": "Message",
        "searchFollowButtonText": "Follow",
        "searchFollowingButtonText": "Unfollow",
        "searchNoResultFoundText": "No result found.",
        
        #Profile
        "profilePageTittle": "Profile",
        "profileRankAIText": "I'M JUST ROBOT",
        "profileRankUserText1": " IN RANKINGS",
        "profileRankUserText2": " NO RANKING",
        "profileFollowButton": "Follow",
        "profileFollowingButton": "Unfollow",
        "profileTitleText1": "42 Kocaeli Student",
        "profileTitleText2": "Software Developer",

        "profileMatchHistoryText1": "Opponent",
        "profileMatchHistoryText2": "Result",
        "profileMatchHistoryText3": "Score",
        "profileMatchHistoryText4": "Duration",

        "profileMatchHistoryWinText": "Win",
        "profileMatchHistoryLoseText": "Lose",

        "profileRankText1": "Rank",

        "profileGameStats1": "Games Played:",
        "profileGameStats2": "Wins:",
        "profileGameStats3": "Loses:",
        "profileGameStats4": "Win Rate:",
        "profileGameStats5": "Win Streak:",
        "profileGameStats6": "Average Game Duration:",
        
        #Friends
        "friendsPageTittle": "Friends",
        "friendsMessageButtonText": "Message",
        "friendsNoResultFoundText": "No result found.",
        
        #ProfileSettings
        "profileSettingsPageTittle": "Profile Settings",
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
            "changePassword42Text": "Since you are logged in with 42, your password setting feature is disabled.",
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
            "blockedStatusText": "Blocked",

            #Close-Account
            "closeAccountHeaderText": "Close Account",
            "closeAccountInputText": "Email",
            "closeAccountSubHeaderText": "You can delete your account here. This action is irreversible.",
            "closeAccountButton": "Close Account",
            

    }
    return context

def get_lang_tr():
    context = {
        #index
        "basePageTittle": "Indian-Pong",
        "baseHeaderText": "Indian-Pong",
        "baseSubHeaderText": "Indian-Pong Hintli geliştiriciler tarafından 42 okulu için geliştirilmiştir!",
        "basePlayButtonText": "YOLCULUĞA BAŞLA!",

        "baseInfoHeaderText": "Indian-Pong'a hoş geldiniz!",
        "baseInfoHeaderDescription": "Pong, klasik masa tenisi oyununun heyecanını ve rekabetini internet ortamına taşıyor. Bu platformda hem eğlenebilir hem de yeteneğini konuşturabilir, sıralamada yükselip en iyiler arasına girebilirsin.",
        "baseInfoSubHeaderText": "Oyna ve Kazan",
        "baseInfoSubHeaderDescription1": "Her oyun kazandığında Pong Point kazanarak sıralamada yüksel.",
        "baseInfoSubHeaderDescription2": "Kazançlarınla mağazadan yeni eşyalar, raket ve masalar satın alarak oyun deneyimini geliştir.",
        "baseInfoSubHeaderText2": "Hemen Başla",
        "baseInfoSubHeaderDescription3": "Hesap oluşturarak profilini kişiselleştir, istatistiklerini takip et ve sıralamadaki yerini gör.",
        "baseInfoSubHeaderText3": "Daha Fazlası",
        "baseInfoSubHeaderDescription4": "Turnuvalara katılarak rakiplerinle yüzleş.",
        "baseInfoSubHeaderDescription5": "Arkadaşlarınla özel oyunlar kurarak keyifli vakit geçir.",
        "baseInfoSubHeaderDescription6": "Diğer oyuncularla sohbet et, taktikler paylaş ve Pong topluluğuna katıl.",

        #Login
        "loginPageTittle": "Giriş Yap",
        "loginHeaderText1": "Hoş geldiniz,",
        "loginHeaderText2": "devam etmek için giriş yapın",
        "loginInputUsernameText": "Kullanıcı Adı",
        "loginInputPasswordText": "Şifre",
        "loginForgotPasswordText": "Şifremi Unuttum?",
        "loginButtonLogin": "Giriş Yap",
        "loginButtonJoin": "Üye Ol",

        #404
        "notFoundPageTittle": "Sayfa Bulunamadı",
        "notFoundHeaderText": "404 HATA",
        "notFoundSubHeaderText": "Muhtemelen sitemizde kayboldunuz!",
        
        #Signup
        "signupPageTittle": "Kayıt Ol",
        "signupHeaderText1": "Hoş geldiniz,",
        "signupHeaderText2": "devam etmek için kayıt olun",
        "signupInputUsernameText": "Kullanıcı Adı",
        "signupInputDisplayNameText": "Görünen Ad",
        "signupInputEmailText": "E-posta",
        "signupInputPasswordText": "Şifre",
        "signupInputConfirmPasswordText": "Şifreyi Onayla",
        "signupImageUploadText": "Resim Yükle",
        "signupButtonSignup": "Kayıt Ol",

        #ForgotPassword
        "forgotPasswordPageTittle": "Şifremi Unuttum",
        "forgotPasswordHeaderText": "Şifremi Unuttum",
        "forgotPasswordInputEmailText": "E-posta",
        "forgotPasswordButtonSend": "E-posta Gönder",
        "forgotPasswordLinkText": "Hesabınız yok mu?",
        "forgotPasswordLinkButtonText": "Kayıt Ol",

        #ChangePassword
        "changePasswordPageTittle": "Şifre Değiştir",
        "changePasswordHeaderText": "Şifre Değiştir",
        "changePassswordSubHeaderText": "şifreni değiştir",

        #Dashboard
        "dashboardPageTittle": "Ana Sayfa",
        "dashboardText1": "HOŞ GELDİNİZ, ",
        "dashboardText2": "Indian Pong, 42 okulu toplulugu için geliştirilmiş bir takım projesidir ve klasik Atari oyunu Ping-Pong ile nostaljik bir oyun deneyimi sunar. Bu platform, kullanıcıların birbirleriyle Ping-Pong maçlari yapmalarina olanak tanır ve dostane rekabet ortamı oluşturur. Oyun deneyimi dışında, Indian Pong, kullanıcıların birbirleriyle iletişim kurabileceği ve bağlanti kurabilecegi sohbet odalarını içeren bir sosyal boyut sunar. Platform ayrıca, kullanicilarin 42 okulu topluluğunda arkadaş ekleyerek ağlarını genişletmelerine olanak tanır. Genel olarak, Indian Pong, retro oyun keyfini modern sosyal etkileşimle birleştirerek, 42 okulu topluluğu icin canlı ve etkileşimli bir deneyim sunar.",

        "dashboardGamesPlayed": "Oynanan Oyunlar",
        "dashboardWinCount": "Kazanma Sayısı",
        "dashboardWinStreak": "Kazanma Serisi",
        "dashboardLoseStreak": "Kaybetme Serisi",
        "dashboardWinRate": "Kazanma Oranı",
        "dashboardAverageGameDuration": "Ortalama Oyun Süresi",
        "dashboardAveragePointsWon": "Ortalama Kazanılan Puanlar",
        "dashboardAveragePointsLost": "Ortalama Kaybedilen Puanlar",

        
        #Pong-Game
        "pongGamePageTittle": "Pong Oyunu",
        "pongGameHeaderText": "Pong Lobisine Hoş Geldiniz",
        "pongGameSubHeaderText": "Yapay Zeka ile oynayarak kendinizi geliştirebilir. Gerçek bir kişiyle oynamak istiyorsanız, diğer seçeneği düşünün; 5 dakika içinde eşleşecek birini bulamazsak, eşleşme iptal edilecektir. Unutmadan önce iyi şanslar!",
        "pongGameAIButtonText": "Yapay Zeka Oyunu",
        "pongGameLocalButtonText": "Yerel Oyun",
        "pongGameRemoteButtonText": "Uzak Oyuncu",
        "pongGameLocalTournamentButtonText": "Yerel Turnuva",
        "pongGameTournamentButtonText": "Turnuva",

            #AI-Game
            "aiGamePageTittle": "Pong Yapay Zeka Oyunu",
            "aiGameReactionDelayText": "Tepki Gecikmesi",
            "aiGameGetReadyText": "Hazir Ol",
            "aiGamePresSpaceText": "'Space' tusuna basarak basla",
            "aiGameCountdownText": "Basliyor",

            "aiGameGameOverText": "Oyun Bitti",
            "aiGameRestartButtonText": "Yeniden",
            "aiGameExitButtonText": "Cikis",

            "aiGameInfoHeaderText": "Oyun Hakkında",
            "aiGameInfoSubHeaderText": "Oyunu Nasıl Oynarım?",
            "aiGameInfoSubHeaderDescription1": "Pong oyununda oyuncular rakiplerine karsı bir masa tenisi macı yaparlar. W-A-S-D tusları (veya yukarı-asagı-sol-sag ok tusları) topu kontrol etmek icin kullanılır.",
            "aiGameInfoSubHeaderText2": "Kazan ve Geliş",
            "aiGameInfoSubHeaderDescription2": "Her oyun kazandığında Pong Puan kazanırsın. Bu puanlarla mağazadan yeni eşyalar, raket ve masalar satın alarak oyun deneyimini geliştirebilirsin.",
            "aiGameInfoSubHeaderText3": "Hemen Başla",
            "aiGameInfoSubHeaderDescription3": "Hesap oluşturarak oyun deneyimini kişiselleştirebilirsin. Bir hesapla istatistiklerini takip edebilir ve sıralamandaki yerini görebilirsin.",
            "aiGameInfoSubHeaderText4": "Daha Fazlası",
            "aiGameInfoSubHeaderDescription4": "Rakiplerinle yüzleşmek ve becerilerini test etmek icin turnuvalara katılabilirsin. Ayrıca arkadaşlarınla özel oyunlar oluşturabilir ve Pong topluluğuna katılabilirsin.",

            "aiGameInfoSubHeaderText5": "Kontroller",
            "aiGameInfoSubHeaderDescription5": "Yukarı",
            "aiGameInfoSubHeaderDescription6": "Aşağı",
            "aiGameInfoSubHeaderText6": "Yetenekler",
            "aiGameInfoSubHeaderDescription7": "Bir Hilekar Gibi",
            "aiGameInfoSubHeaderDescription8": "Hızlı ve Öfkeli",
            "aiGameInfoSubHeaderDescription9": "Dondurulmuş Top",

            #Local-Game
            "localGamePageTittle": "Yerel Oyun",
            "localGameHeaderText": "1v1 Yerel Oyun",
            "localGamePlayer1Text": "1. Oyuncu Adi",
            "localGamePlayer2Text": "2. Oyuncu Adi",
            "localGameMaxScoreText": "Maksimum Skor",
            "localGameGameModeText": "Oyun Modu",
            "localGameChooseModeText1": "Klasik",
            "localGameChooseModeText2": "Yetenekler",
            "localGameButtonStart": "Basla",

            #Local-Tournament
            "localTournamentPageTittle": "Yerel Turnuva",
            "localTournamentGameHeaderText": "Yerel Turnuva",
            "localTournamentPlayer1Text": "1. Oyuncu Adi",
            "localTournamentPlayer2Text": "2. Oyuncu Adi",
            "localTournamentPlayer3Text": "3. Oyuncu Adi",
            "localTournamentPlayer4Text": "4. Oyuncu Adi",  
            "localTournamentMaxScoreText": "Maksimum Skor",
            "localTournamentGameModeText": "Oyun Modu",
            "localTournamentChooseModeText1": "Klasik",
            "localTournamentChooseModeText2": "Yetenekler",
            "localTournamentButtonStart": "Baslat & Eslesme",
            "localTournamentBracketTitle": "Turnuva Eslesmesi",
            "localTournamentBracketStartButtonText": "Turnuvayi Baslat",
            "localTournamentTournamentOverText": "Turnuva Bitti",
            "localTournamentOverButtonText": "Bitti",

            "localTournamentNextButtonText": "Sonraki",

            #Tournament
            "tournamentPageTittle": "Turnuva",
            "tournamentHeaderText": "Pong için Turnuva Lobisine Hoş Geldiniz",
            "tournamentSubHeaderText": "Burada bir turnuva lobisine katılabilir veya kendi turnuva lobinizi oluşturabilirsiniz. Odanızı oluşturduktan sonra davet kodunu paylaşarak arkadaşlarınızı davet edebilirsiniz. Unutmadan önce iyi şanslar!",
            "tournamentJoinButtonText": "Turnuvaya Katıl",
            "tournamentCreateButtonText": "Turnuva Oluştur",

            #Tournament-Create
            "tournamentCreatePageTittle": "Turnuva Oluştur",
            "tournamentCreateHeaderText": "TURNUVA OLUŞTUR",
            "tournamentCreateSubHeaderText": "Bir turnuva oluşturmak için bir turnuva adına ve her oyunun maksimum kaç puan alacağına ihtiyacım var. Unutmadan önce iyi şanslar!",
            "tournamentCreateNameText": "Turnuva Adı",
            "tournamentCreateMaxPointsText": "Oyun Başına Maksimum Skor",
            "tournamentCreateGameModeText": "Oyun Modu",
            "tournamentCreateChooseModeText1": "Klasik",
            "tournamentCreateChooseModeText2": "Yetenekler",
            "tournamentCreateButtonCreate": "Turnuva Oluştur",

            #Joined-Tournament-Room
            "tournamentroomPageTittle": "Turnuva Odası",
            "tournamentroomHeaderText": "Turnuva Odası",
            "tournamentroomRoomText": "Oda",
            "tournamentroomLeaveButtonText": "TURNUVADAN AYRIL",
            "tournamentroomStartButtonText": "TURNUVAYI BAŞLAT",
            "tournamentroomJoinButtonText": "TURNUVAYA KATIL",
            "tournamentCheckBracketButtonText": "BRAKETI GÖRÜNTÜLE",
            "tournamentroomTournamentRoomButton": "TURNUVA ODASI",
            "tournamentroomWaitingText": "Bekleniyor,",
            "tournamentroomForPlayerText": " oyuncu...",

            #Tournament Room List
            "tournamentRoomListPageTittle": "Turnuva Odaları",
            "tournamentRoomListHeaderText": "Turnuva Odaları",


        #RPS Game
        "rpsGamePageTittle": "Taş Kağıt Makas",
        "rpsGameText1": "Taş Taş Kağıt Makas Lobisine Hoş Geldiniz",
        "rpsGameText2": "Yapay Zeka ile oynayarak kendinizi geliştirebilir. Gerçek bir kişiyle oynamak istiyorsanız, diğer seçeneği düşünün; 5 dakika içinde eşleşecek birini bulamazsak, eşleşme iptal edilecektir. Unutmadan önce iyi şanslar!",
        "rpsGameAIButtonText": "Yapay Zeka Oyunu",
        "rpsGameLocalButtonText": "Yerel Oyun",
        "rpsGameSearchOpponentButtonText": "Rakip Arayın ",
            
            #AI-Game
            "rpsGamePageTittle": "RPS Yapay Zeka Oyunu",
            "rpsGameScoreText": "skor",
            "rpsGameRockText": "TAŞ",
            "rpsGamePaperText": "KAĞIT",
            "rpsGameScissorsText": "MAKAS",
            "rpsGamePickedText": "seçtin",
            "rpsGamePickedText2": "rakibin seçti",
            "rpsGameAgainText": "tekrar oyna",
            "rpsGameGameOverText": "Oyun Bitti",
            "rpsGameRestartButtonText": "Yeniden",
            "rpsGameExitButtonText": "Çıkış",


        #Rankings
        "rankingsPageTittle": "Sıralamalar",
        "rankingsTableRankText": "Sıra",
        "rankingsTableNameText": "Ad",
        "rankingsTableUsernameText": "Kullanıcı Adı",
        "rankingsTableWinsText": "Kazanmalar",
        "rankingsTableLossesText": "Kayıplar",
        "rankingsTableWinRateText": "Kazanma Yüzdesi",
        "rankingsTablePongPointsText": "Pong Puanı",

        #Store
        "storePageTittle": "Mağaza",
        "storeText": "Mağaza",
        "storeTagText": "Tümü",
        "storeWalletText": "Cüzdan",
        "storeWalleinfoText1": "Oyun oynayarak ",
        "storeWalleinfoText2": " kazanabilirsin.",

        #Inventory
        "inventoryPageTittle": "Envanter",
        "inventoryText": "Envanter",
        "inventoryTagText": "Tümü",
        "inventoryWalletText": "Cüzdan",
        "inventoryWalleinfoText1": "Oyun oynayarak ",
        "inventoryWalleinfoText2": " kazanabilirsin.",
        "inventoryModalHeaderText": "Öğeyi Ayarla",
        "inventoryModalSaveButton": "Kaydet",
        "inventoryModalCloseButton": "Kapat",
        "inventoryItemKeyboardInfoText": "Yetenek kullanmak için",
        "inventoryItemKeyboardInfoText2": "tuşunu kullan. Unutma, bu yeteneği kullanabilmek için kuşanmalısın.",
        "inventoryItemKeyboardInfoText3": "Bu öğe için özel bir tuş takımı yok, otomatik olarak kullanılır.",

        
        #Search
        "searchPageTittle": "Arama",
        "searchInputText": "E-posta, kullanıcı adı veya görünen ad ara...",
        "searchMessageButtonText": "Mesaj Gönder",
        "searchFollowButtonText": "Takip Et",
        "searchFollowingButtonText": "Takipten Çık",
        "searchNoResultFoundText": "Sonuç bulunamadı.",
        
        #Profile
        "profilePageTittle": "Profili",
        "profileRankAIText": "SADECE ROBOTUM",
        "profileRankUserText1": " SIRALAMADA",
        "profileRankUserText2": " SIRALAMA YOK",
        "profileFollowButton": "Takip Et",
        "profileFollowingButton": "Takipten Çık",
        "profileTitleText1": "42 Kocaeli Öğrencisi",
        "profileTitleText2": "Yazılım Geliştirici",

        "profileMatchHistoryText1": "Rakip",
        "profileMatchHistoryText2": "Sonuç",
        "profileMatchHistoryText3": "Puan",
        "profileMatchHistoryText4": "Süre",

        "profileMatchHistoryWinText": "Kazandı",
        "profileMatchHistoryLoseText": "Kaybetti",

        "profileRankText1": "Sıra",

        "profileGameStats1": "Oynanan Oyunlar:",
        "profileGameStats2": "Kazanmalar:",
        "profileGameStats3": "Kayıplar:",
        "profileGameStats4": "Kazanma Oranı:",
        "profileGameStats5": "Kazanma Serisi:",
        "profileGameStats6": "Ortalama Oyun Süresi:",
        
        #Friends
        "friendsPageTittle": "Arkadaşlar",
        "friendsMessageButtonText": "Mesaj Gönder",
        "friendsNoResultFoundText": "Sonuç bulunamadı.",
        
        #ProfileSettings
        "profileSettingsPageTittle": "Profil Ayarları",
        "profileSettingsNavbar1": "Profili Düzenle",
        "profileSettingsNavbar2": "Şifre Değişitr",
        "profileSettingsNavbar3": "Sosyal Medya Ekle",
        "profileSettingsNavbar4": "Engellenen Kullanıcılar",
        "profileSettingsNavbar5": "Hesabı Kapat",

            #Edit-Profile
            "editProfileChangeImageText": "Resmi Değiştir",
            "editProfileUsernameText": "Kullanıcı Adı (sitenin diğer kullanıcıları tarafından nasık görüneceği)",
            "editProfileEmailText": "E-posta",
            "editProfile42EmailText": "42 ile oturum açtığınız için e-posta ayarlama özelliği devre dışı bırakılmıştır.",
            "editProfileDisplayNameText": "Görünen Ad",
            "editProfileSaveButtonText": "Değişiklikleri Kaydet",
            
            #Change-Passwordg
            "changePasswordCurrentPasswordText": "Mevcut Şifre",
            "changePasswordNewPasswordText": "Yeni Şifre",
            "changePasswordNewConfirmPasswordText": "Yeni Şifreyi Onayla",
            "changePassword42Text": "42 ile oturum açtığınız için şifre ayarlama özelliği devre dışı bırakılmıştır.",
            "changePasswordSaveButtonText": "Şifreyi Kaydet",
            
            #Add-Socials
            "addSocialsLinkedinInputText": "LinkedIn kullanıcı adınızı girin",
            "addSocialsTwitterInputText": "Twitter kullanıcı adınızı girin",
            "addSocialsGithubInputText": "Github kullanıcı adınızı girin",
            "addSocialsIntraInputText": "42 Intra kullanıcı adınızı girin",
            "addSocialsSaveButtonText": "Sosyal Medyaları Kaydet",

            #Blocked-Users
            "blockedUsersHeaderText": "Engellenen Hesaplar",
            "blockedUsersSubHeaderText": "Burada engellediğiniz hesapları açabilirsiniz.",
            "blockedStatusText": "Engellendi",

            #Close-Account
            "closeAccountHeaderText": "Hesabı Kapat",
            "closeAccountInputText": "E-posta",
            "closeAccountSubHeaderText": "Burada hesabınızı silebilirsiniz. Bu işlem geri alinamaz.",
            "closeAccountButton": "Hesabı Kapat",
            

    }
    return context


def get_lang_pt():
    context = {
        #index
        "basePageTittle": "Indian-Pong",
        "baseHeaderText": "Indian-Pong",
        "baseSubHeaderText": "A versão indiana do clássico jogo Pong",
        "basePlayButtonText": "Vamos Comecar!",

        "baseInfoHeaderText": "Bem-vindo ao Indian-Pong!",
        "baseInfoHeaderDescription": "Pong traz a emoção e a competição do tênis de mesa clássico para a internet. Nesta plataforma, você pode se divertir, mostrar suas habilidades e subir no ranking para se tornar um dos melhores.",
        "baseInfoSubHeaderText": "Jogue e Ganhe",
        "baseInfoSubHeaderDescription1": "Ganhe Pong Points a cada jogo que vencer para subir no ranking.",
        "baseInfoSubHeaderDescription2": "Use seus ganhos para comprar novos itens, raquetes e mesas da loja para aprimorar sua experiência de jogo.",
        "baseInfoSubHeaderText2": "Comece Agora",
        "baseInfoSubHeaderDescription3": "Crie uma conta para personalizar seu perfil, acompanhar suas estatísticas e ver onde você está no ranking.",
        "baseInfoSubHeaderText3": "Mais Recursos",
        "baseInfoSubHeaderDescription4": "Participe de torneios para enfrentar seus oponentes.",
        "baseInfoSubHeaderDescription5": "Divirta-se com seus amigos hospedando jogos privados.",
        "baseInfoSubHeaderDescription6": "Converse com outros jogadores, compartilhe táticas e participe da comunidade Pong.",

        #Login
        "loginPageTittle": "Iniciar sessão",
        "loginHeaderText1": "Bem-vindo,",
        "loginHeaderText2": "faca login para continuar",
        "loginInputUsernameText": "Nome de Usuário",
        "loginInputPasswordText": "Senha",
        "loginForgotPasswordText": "Esqueceu a Senha?",
        "loginButtonLogin": "Vamos lá",
        "loginButtonJoin": "Junte-se",

        #404
        "notFoundPageTittle": "Página não encontrada",
        "notFoundHeaderText": "404 ERRO",
        "notFoundSubHeaderText": "Você provavelmente se perdeu em nosso site!",
        
        #Signup
        "signupPageTittle": "Inscreva-se",
        "signupHeaderText1": "Bem-vindo,",
        "signupHeaderText2": "inscreva-se para continuar",
        "signupInputUsernameText": "Nome de Usuário",
        "signupInputDisplayNameText": "Nome de Exibicão",
        "signupInputEmailText": "E-mail",
        "signupInputPasswordText": "Senha",
        "signupInputConfirmPasswordText": "Senha (novamente)",
        "signupImageUploadText": "Imagem",
        "signupButtonSignup": "Vamos!",

        #ForgotPassword
        "forgotPasswordPageTittle": "Esqueceu a Senha",
        "forgotPasswordHeaderText": "Esqueceu a Senha",
        "forgotPasswordInputEmailText": "E-mail",
        "forgotPasswordButtonSend": "Enviar E-mail",
        "forgotPasswordLinkText": "Não tem uma conta?",
        "forgotPasswordLinkButtonText": "Junte-se a Nós",

        #ChangePassword
        "changePasswordPageTittle": "Mudar Senha",
        "changePasswordHeaderText": "Mudar Senha",
        "changePassswordSubHeaderText": "alterar a sua palavra-passe",


        #Dashboard
        "dashboardPageTittle": "Painel",
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
        "pongGamePageTittle": "Jogo de Pong",
        "pongGameHeaderText": "Bem-vindo ao Lobby de Pong",
        "pongGameSubHeaderText": "Podes melhorar o teu desempenho jogando com a Inteligência Artificial. Se quiseres jogar com uma pessoa real, considera a outra opção; se não encontrarmos alguém com quem jogar no espaço de 5 minutos, o jogo será cancelado. Boa sorte antes que nos esqueçamos!",
        "pongGameAIButtonText": "Jogar com a IA",
        "pongGameLocalButtonText": "Jogo Local",
        "pongGameRemoteButtonText": "Jogador Remoto",
        "pongGameLocalTournamentButtonText": "Locais Torneio",
        "pongGameTournamentButtonText": "Torneio",

            #AI-Game
            "aiGamePageTittle": "Jogo de Pong com a IA",
            "aiGameReactionDelayText": "Atraso na Reacão",
            "aiGameGetReadyText": "Prepare-se",
            "aiGamePresSpaceText": "Pressione 'Espaco' para iniciar",
            "aiGameCountdownText": "Iniciando em",

            "aiGameGameOverText": "Fim de Jogo",
            "aiGameRestartButtonText": "Reiniciar",
            "aiGameExitButtonText": "Sair",

            "aiGameInfoHeaderText": "Sobre o Jogo",
            "aiGameInfoSubHeaderText": "Como Jogar o Jogo?",
            "aiGameInfoSubHeaderDescription1": "No jogo Pong, os jogadores participam de uma partida de tênis de mesa contra seus oponentes. As teclas W-A-S-D (ou as setas cima-baixo-esquerda-direita) são usadas para controlar a bola.",
            "aiGameInfoSubHeaderText2": "Ganhe e Melhore",
            "aiGameInfoSubHeaderDescription2": "Você ganha Pong Points a cada jogo que vence. Com esses pontos, você pode comprar novos itens, raquetes e mesas da loja para aprimorar sua experiência de jogo.",
            "aiGameInfoSubHeaderText3": "Comece Agora",
            "aiGameInfoSubHeaderDescription3": "Você pode criar uma conta para personalizar sua experiência de jogo. Com uma conta, você pode acompanhar suas estatísticas e ver sua posição no ranking.",
            "aiGameInfoSubHeaderText4": "Mais Recursos",
            "aiGameInfoSubHeaderDescription4": "Você pode participar de torneios para enfrentar seus oponentes e testar suas habilidades. Além disso, você pode criar jogos privados com seus amigos e se juntar à comunidade Pong.",
            
            "aiGameInfoSubHeaderText5": "Controles",
            "aiGameInfoSubHeaderDescription5": "Cima",
            "aiGameInfoSubHeaderDescription6": "Baixo",
            "aiGameInfoSubHeaderText6": "Habilidades",
            "aiGameInfoSubHeaderDescription7": "Como um Trapaceiro",
            "aiGameInfoSubHeaderDescription8": "Veloz e Furioso",
            "aiGameInfoSubHeaderDescription9": "Bola Congelada",

            #Local-Game
            "localGamePageTittle": "Jogo Local",
            "localGameHeaderText": "Jogo Local 1v1",
            "localGamePlayer1Text": "Nome do Jogador 1",
            "localGamePlayer2Text": "Nome do Jogador 2",
            "localGameMaxScoreText": "Pontuacão Máxima",
            "localGameGameModeText": "Modo de Jogo",
            "localGameChooseModeText1": "Vanilla",
            "localGameChooseModeText2": "Habilidades",
            "localGameButtonStart": "Iniciar",

            #Local-Tournament
            "localTournamentPageTittle": "Torneio Local",
            "localTournamentGameHeaderText": "Torneio Local",
            "localTournamentPlayer1Text": "Nome do Jogador 1",
            "localTournamentPlayer2Text": "Nome do Jogador 2",
            "localTournamentPlayer3Text": "Nome do Jogador 3",
            "localTournamentPlayer4Text": "Nome do Jogador 4",  
            "localTournamentMaxScoreText": "Pontuacão Máxima",
            "localTournamentGameModeText": "Modo de Jogo",
            "localTournamentChooseModeText1": "Vanilla",
            "localTournamentChooseModeText2": "Habilidades",
            "localTournamentButtonStart": "Iniciar & Empar.",
            "localTournamentBracketTitle": "Empar. Torneio",
            "localTournamentBracketStartButtonText": "Iniciar Torneio",
            "localTournamentTournamentOverText": "Torneio Terminado",
            "localTournamentOverButtonText": "Terminado",

            "localTournamentNextButtonText": "Próximo",

            #Tournament
            "tournamentPageTittle": "Torneio",
            "tournamentHeaderText": "Bem-vindo ao Lobby do Torneio de Pong",
            "tournamentSubHeaderText": "Aqui você pode entrar em um lobby de torneio ou criar seu próprio lobby de torneio. Você pode convidar seus amigos compartilhando o código de convite após criar a sala. Boa sorte antes que eu esqueca!",
            "tournamentJoinButtonText": "Entrar no Torneio",
            "tournamentCreateButtonText": "Criar Torneio",

            #Tournament-Create
            "tournamentCreatePageTittle": "Criar Torneio",
            "tournamentCreateHeaderText": "CRIAR TORNEIO",
            "tournamentCreateSubHeaderText": "Para criar um torneio, eu preciso de um nome de torneio, quantos pontos máximos cada jogo terá. Boa sorte antes que eu esqueca!",
            "tournamentCreateNameText": "Nome do Torneio",
            "tournamentCreateMaxPointsText": "Pontuacão Máxima dos Jogos",
            "tournamentCreateGameModeText": "Modo de Jogo",
            "tournamentCreateChooseModeText1": "Vanilla",
            "tournamentCreateChooseModeText2": "Habilidades",
            "tournamentCreateButtonCreate": "Criar Torneio",

            #Joined-Tournament-Room
            "tournamentroomPageTittle": "Sala de Torneio",
            "tournamentroomHeaderText": "Sala de Torneio",
            "tournamentroomRoomText": "Sala",
            "tournamentroomLeaveButtonText": "SAIR DO TORNEIO",
            "tournamentroomStartButtonText": "INICIAR TORNEIO",
            "tournamentroomJoinButtonText": "ENTRAR NO TORNEIO",
            "tournamentCheckBracketButtonText": "VER BRACKET",
            "tournamentroomTournamentRoomButton": "SALA DE TORNEIO",
            "tournamentroomWaitingText": "Aguardando,",
            "tournamentroomForPlayerText": "jogadores...",

            #Tournament Room List
            "tournamentRoomListPageTittle": "Salas de Torneio",
            "tournamentRoomListHeaderText": "Salas de Torneio",

        #RPS Game
        "rpsGamePageTittle": "Pedra, Papel e Tesoura",
        "rpsGameText1": "Bem-vindo ao Lobby de Pedra, Papel e Tesoura",
        "rpsGameText2": "Podes melhorar o teu desempenho jogando com a Inteligência Artificial. Se quiseres jogar com uma pessoa real, considera a outra opção; se não encontrarmos alguém com quem jogar no espaço de 5 minutos, o jogo será cancelado. Boa sorte antes que nos esqueçamos!",
        "rpsGameAIButtonText": "Jogar com a IA",
        "rpsGameLocalButtonText": "Jogo Local",
        "rpsGameSearchOpponentButtonText": "Buscar Oponente ",

        #AI-Game
            "rpsGamePageTittle": "Jogo de Pedra, Papel e Tesoura com Inteligência Artificial",
            "rpsGameScoreText": "pontuação",
            "rpsGameRockText": "PEDRA",
            "rpsGamePaperText": "PAPEL",
            "rpsGameScissorsText": "TESOURA",
            "rpsGamePickedText": "escolheste",
            "rpsGamePickedText2": "o adversário escolheu",
            "rpsGameAgainText": "jogar novamente",
            "rpsGameGameOverText": "Jogo Terminado",
            "rpsGameRestartButtonText": "Reiniciar",
            "rpsGameExitButtonText": "Sair",

        #Rankings
        "rankingsPageTittle": "Classificacão",
        "rankingsTableRankText": "Classificacão",
        "rankingsTableNameText": "Nome",
        "rankingsTableUsernameText": "Nome de Usuário",
        "rankingsTableWinsText": "Vitórias",
        "rankingsTableLossesText": "Derrotas",
        "rankingsTableWinRateText": "Taxa de Vitória",
        "rankingsTablePongPointsText": "Pontos Pong",

        #Store
        "storePageTittle": "Loja",
        "storeText": "Loja",
        "storeTagText": "Tudo",
        "storeWalletText": "Carteira",
        "storeWalleinfoText1": "Você pode ganhar ",
        "storeWalleinfoText2": " jogando.",

        #Inventory
        "inventoryPageTittle": "Inventário",
        "inventoryText": "Inventário",
        "inventoryTagText": "Tudo",
        "inventoryWalletText": "Carteira",
        "inventoryWalleinfoText1": "Você pode ganhar ",
        "inventoryWalleinfoText2": " jogando.",
        "inventoryModalHeaderText": "Definir Item",
        "inventoryModalSaveButton": "Salvar",
        "inventoryModalCloseButton": "Fechar",
        "inventoryItemKeyboardInfoText": "Use a tecla",
        "inventoryItemKeyboardInfoText2": "para usar essa habilidade. E lembre-se, você deve equipar essa habilidade.",
        "inventoryItemKeyboardInfoText3": "Este item não tem um teclado personalizado, é usado automaticamente.",

        
        #Search
        "searchPageTittle": "Procurar",
        "searchInputText": "Procurar por e-mail, nome de usuário ou nome de exibicão...",
        "searchMessageButtonText": "Mensagem",
        "searchFollowButtonText": "Seguir",
        "searchFollowingButtonText": "Deixar",
        "searchNoResultFoundText": "Nenhum resultado encontrado.",
        
        #Profile
        "profilePageTittle": "Perfil",
        "profileRankAIText": "APENAS ROBÔ",
        "profileRankUserText1": " RANKING",
        "profileRankUserText2": " SEM RANKING",
        "profileFollowButton": "Seguir",
        "profileFollowingButton": "Deixar",
        "profileTitleText1": "Estudante da 42 Kocaeli",
        "profileTitleText2": "Desenvolvedor de Software",

        "profileMatchHistoryText1": "Oponente",
        "profileMatchHistoryText2": "Resultado",
        "profileMatchHistoryText3": "Pontos",
        "profileMatchHistoryText4": "Tempo",

        "profileMatchHistoryWinText": "Venceu",
        "profileMatchHistoryLoseText": "Perdeu",

        "profileRankText1": "Classificacão",

        "profileGameStats1": "Jogos Jogados:",
        "profileGameStats2": "Vitórias:",
        "profileGameStats3": "Derrotas:",
        "profileGameStats4": "Taxa de Vitória:",
        "profileGameStats5": "Sequência de Vitórias:",
        "profileGameStats6": "Duração Média do Jogo:",

        #Friends
        "friendsPageTittle": "Amigos",
        "friendsMessageButtonText": "Mensagem",
        "friendsNoResultFoundText": "Nenhum resultado encontrado.",

        #ProfileSettings
        "profileSettingsPageTittle": "Configurações do Perfil",
        "profileSettingsNavbar1": "Editar Perfil",
        "profileSettingsNavbar2": "Alterar Senha",
        "profileSettingsNavbar3": "Adicionar Redes Sociais",
        "profileSettingsNavbar4": "Usuários Bloqueados",
        "profileSettingsNavbar5": "Fechar Conta",

            #Edit-Profile
            "editProfileChangeImageText": "Alterar Imagem",
            "editProfileUsernameText": "Nome de usuário (como seu nome aparecerá para outros usuários no site)",
            "editProfileEmailText": "Email",
            "editProfile42EmailText": "Como você está logado com 42, o recurso de configuração de e-mail está desativado.",
            "editProfileDisplayNameText": "Nome de Exibição",
            "editProfileSaveButtonText": "Salvar Alterações",

            #Change-Password
            "changePasswordCurrentPasswordText": "Senha Atual",
            "changePasswordNewPasswordText": "Nova Senha",
            "changePasswordNewConfirmPasswordText": "Confirmar Nova Senha",
            "changePassword42Text": "Como você está logado com 42, o recurso de configuração de senha está desativado.",
            "changePasswordSaveButtonText": "Salvar Senha",

            #Add-Socials
            "addSocialsLinkedinInputText": "Insira seu nome de usuário do LinkedIn",
            "addSocialsTwitterInputText": "Insira seu nome de usuário do Twitter",
            "addSocialsGithubInputText": "Insira seu nome de usuário do Github",
            "addSocialsIntraInputText": "Insira seu nome de usuário do 42 Intra",
            "addSocialsSaveButtonText": "Salvar Redes Sociais",

            #Blocked-Users
            "blockedUsersHeaderText": "Contas Bloqueadas",
            "blockedUsersSubHeaderText": "Você pode desbloquear as contas que bloqueou aqui.",
            "blockedStatusText": "Bloqueado",


            #Close-Account
            "closeAccountHeaderText": "Fechar Conta",
            "closeAccountInputText": "E-mail",
            "closeAccountSubHeaderText": "Você pode excluir sua conta aqui. Esta ação é irreversível.",
            "closeAccountButton": "Fechar Conta",
    }
    return context

def get_lang_hi():
    context = {
        #index
        "basePageTittle": "इंडियन-पॉन्ग",
        "baseHeaderText": "इंडियन-पॉन्ग",
        "baseSubHeaderText": "प्रसिद्ध खेल पॉन्ग का भारतीय संस्करण",
        "basePlayButtonText": "शुरू करें!",

        "baseInfoHeaderText": "इंडियन-पॉन्ग में आपका स्वागत है!",
        "baseInfoHeaderDescription": "पॉन्ग इंटरनेट पर क्लासिक टेबल टेनिस खेल के उत्साह और प्रतिस्पर्धा को लाता है। इस प्लेटफ़ॉर्म पर आप मजा कर सकते हैं, अपने कौशल का परिचय दे सकते हैं और शीर्ष में आने के लिए रैंकिंग में चढ़ सकते हैं।",
        "baseInfoSubHeaderText": "खेलें और जीतें",
        "baseInfoSubHeaderDescription1": "जीतने पर प्रत्येक खेल से पॉन्ग पॉइंट्स कमाकर रैंकिंग में चढ़ें।",
        "baseInfoSubHeaderDescription2": "अपनी जीत से नए आइटम, रैकेट और टेबल्स खरीदने के लिए दुकान से खर्च करें।",
        "baseInfoSubHeaderText2": "अभी शुरू करें",
        "baseInfoSubHeaderDescription3": "प्रोफ़ाइल को व्यक्तिगत बनाने, अपने स्टैटिस्टिक्स को ट्रैक करने और रैंकिंग में अपनी जगह देखने के लिए खाता बनाएं।",
        "baseInfoSubHeaderText3": "अधिक सुविधाएं",
        "baseInfoSubHeaderDescription4": "अपने प्रतिद्वंद्वियों के साथ टूर्नामेंट में भाग लेने के लिए।",
        "baseInfoSubHeaderDescription5": "अपने दोस्तों के साथ निजी खेल खेलकर मजा करें।",
        "baseInfoSubHeaderDescription6": "अन्य खिलाड़ियों के साथ चैट करें, रणनीतियाँ साझा करें और पॉन्ग समुदाय में शामिल हों।",

        #Login
        "loginPageTittle": "लॉग इन करें",
        "loginHeaderText1": "स्वागत है,",
        "loginHeaderText2": "जारी रखने के लिए साइन इन करें",
        "loginInputUsernameText": "उपयोगकर्ता नाम",
        "loginInputPasswordText": "पासवर्ड",
        "loginForgotPasswordText": "पासवर्ड भूल गए?",
        "loginButtonLogin": "चलो चलते हैं",
        "loginButtonJoin": "हमारे साथ",

        #404
        "notFoundPageTittle": "पृष्ठ नहीं मिला",
        "notFoundHeaderText": "404 त्रुटि",
        "notFoundSubHeaderText": "आप शायद हमारी वेबसाइट में खो गए हैं!",
        
        #Signup
        "signupPageTittle": "साइन अप करें",
        "signupHeaderText1": "स्वागत है,",
        "signupHeaderText2": "जारी रखने के लिए साइन अप करें",
        "signupInputUsernameText": "उपयोगकर्ता नाम",
        "signupInputDisplayNameText": "डिस्प्ले नाम",
        "signupInputEmailText": "ईमेल",
        "signupInputPasswordText": "पासवर्ड",
        "signupInputConfirmPasswordText": "पासवर्ड (फिर से)",
        "signupImageUploadText": "छवि अपलोड करें",
        "signupButtonSignup": "चमकाओ!",

        #ForgotPassword
        "forgotPasswordPageTittle": "पासवर्ड भूल गए",
        "forgotPasswordHeaderText": "पासवर्ड भूल गए",
        "forgotPasswordInputEmailText": "ईमेल",
        "forgotPasswordButtonSend": "ईमेल भेजें",
        "forgotPasswordLinkText": "खाता नहीं है?",
        "forgotPasswordLinkButtonText": "हमारे साथ शामिल हों",

        #ChangePassword
        "changePasswordPageTittle": "पासवर्ड बदलें",
        "changePasswordHeaderText": "पासवर्ड बदलें",
        "changePassswordSubHeaderText": "अपना पासवर्ड बदलें",


        #Dashboard
        "dashboardPageTittle": "डैशबोर्ड",
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
        "pongGamePageTittle": "पॉन्ग खेल",
        "pongGameHeaderText": "पॉन्ग लॉबी में आपका स्वागत है",
        "pongGameSubHeaderText": "आप आर्टिफिशियल इंटेलिजेंस के साथ खेलकर खुद को बेहतर बना सकते हैं। यदि आप किसी वास्तविक व्यक्ति के साथ खेलना चाहते हैं, तो दूसरे विकल्प पर विचार करें; यदि हमें 5 मिनट के भीतर मैच के लिए कोई नहीं मिल सका, तो मैच रद्द कर दिया जाएगा। इससे पहले कि मैं भूल जाऊँ, शुभकामनाएँ!",
        "pongGameAIButtonText": "ए.आई. के साथ खेलें",
        "pongGameLocalButtonText": "स्थानीय खेल",
        "pongGameRemoteButtonText": "दूरस्थ खिलाड़ी",
        "pongGameLocalTournamentButtonText": "स्थानीय टूर्नामेंट",
        "pongGameTournamentButtonText": "टूर्नामेंट",

            #AI-Game
            "aiGamePageTittle": "ए.आई. के साथ पॉन्ग खेल",
            "aiGameReactionDelayText": "प्रतिक्रिया में देरी",
            "aiGameGetReadyText": "तैयार हो जाओ",
            "aiGamePresSpaceText": "शुरू करने के लिए 'स्पेस' दबाएं",
            "aiGameCountdownText": "में शुरू हो रहा है",

            "aiGameGameOverText": "खेल समाप्त हो गया",
            "aiGameRestartButtonText": "पुनः आरंभ",
            "aiGameExitButtonText": "निकास",

            "aiGameInfoHeaderText": "खेल के बारे में",
            "aiGameInfoSubHeaderText": "खेल कैसे खेलें?",
            "aiGameInfoSubHeaderDescription1": "पॉन्ग खेल में खिलाड़ी अपने प्रतिद्वंद्वी के खिलाफ एक टेनिस की मैच खेलते हैं। W-A-S-D (या ऊपर-नीचे-बाएं-दाएं तीर) तीरों को नियंत्रित करने के लिए उपयोग किया जाता है।",
            "aiGameInfoSubHeaderText2": "जीतें और सुधारें",
            "aiGameInfoSubHeaderDescription2": "आप हर जीते खेल के बाद पॉन्ग पॉइंट्स कमाते हैं। इन पॉइंट्स के साथ आप खेल का अनुभव बेहतर बनाने के लिए दुकान से नए आइटम, रैकेट और टेबल खरीद सकते हैं।",
            "aiGameInfoSubHeaderText3": "अभी शुरू करें",
            "aiGameInfoSubHeaderDescription3": "आप अपने खेल का अनुभव व्यक्तिगत करने के लिए एक खाता बना सकते हैं। एक खाते के साथ, आप अपने स्टैटिस्टिक्स को ट्रैक कर सकते हैं और रैंकिंग में अपनी जगह देख सकते हैं।",
            "aiGameInfoSubHeaderText4": "अधिक सुविधाएं",
            "aiGameInfoSubHeaderDescription4": "आप अपने प्रतिद्वंद्वियों के साथ टूर्नामेंट में भाग लेने के लिए और अपने कौशल का परीक्षण करने के लिए टूर्नामेंट में भाग ले सकते हैं। इसके अलावा, आप अपने दोस्तों के साथ निजी खेल बना सकते हैं और पॉन्ग समुदाय में शामिल हो सकते हैं।",

            "aiGameInfoSubHeaderText5": "नियंत्रण",
            "aiGameInfoSubHeaderDescription5": "ऊपर",
            "aiGameInfoSubHeaderDescription6": "नीचे",
            "aiGameInfoSubHeaderText6": "कौशल",
            "aiGameInfoSubHeaderDescription7": "जैसे एक धोखेबाज",
            "aiGameInfoSubHeaderDescription8": "तेज और उत्तेजित",
            "aiGameInfoSubHeaderDescription9": "जमीन गेंद",

            #Local-Game
            "localGamePageTittle": "स्थानीय खेल",
            "localGameHeaderText": "1v1 स्थानीय खेल",
            "localGamePlayer1Text": "प्लेयर1 नाम",
            "localGamePlayer2Text": "प्लेयर2 नाम",
            "localGameMaxScoreText": "अधिकतम स्कोर",
            "localGameGameModeText": "खेल मोड",
            "localGameChooseModeText1": "वनिला",
            "localGameChooseModeText2": "क्षमताएँ",
            "localGameButtonStart": "प्रारंभ करें",

            #Local-Tournament
            "localTournamentPageTittle": "स्थानीय टूर्नामेंट",
            "localTournamentGameHeaderText": "स्थानीय टूर्नामेंट",
            "localTournamentPlayer1Text": "1. खिलाड़ी नाम",
            "localTournamentPlayer2Text": "2. खिलाड़ी नाम",
            "localTournamentPlayer3Text": "3. खिलाड़ी नाम",
            "localTournamentPlayer4Text": "4. खिलाड़ी नाम",  
            "localTournamentMaxScoreText": "अधिकतम स्कोर",
            "localTournamentGameModeText": "खेल मोड",
            "localTournamentChooseModeText1": "वनिला",
            "localTournamentChooseModeText2": "क्षमताएँ",
            "localTournamentButtonStart": "टूर्नामेंट शुरू करें",
            "localTournamentBracketTitle": "ब्रैकेट",
            "localTournamentBracketStartButtonText": "टूर्नामेंट शुरू करें",
            "localTournamentTournamentOverText": "टूर्नामेंट खत्म हो गया",
            "localTournamentOverButtonText": "खत्म करें",


            "localTournamentNextButtonText": "अगला",

            #Tournament
            "tournamentPageTittle": "टूर्नामेंट",
            "tournamentHeaderText": "पॉन्ग के टूर्नामेंट लॉबी में आपका स्वागत है",
            "tournamentSubHeaderText": "यहां आप एक टूर्नामेंट लॉबी में शामिल हो सकते हैं या अपनी खुद की टूर्नामेंट लॉबी बना सकते हैं। आप अपने दोस्तों को रुम बनाने के बाद इनवाइट कोड साझा करके इन्वाइट कर सकते हैं। भूलने से पहले शुभकामनाएं!",
            "tournamentJoinButtonText": "टूर्नामेंट में शामिल हों",
            "tournamentCreateButtonText": "टूर्नामेंट बनाएं",

            #Tournament-Create
            "tournamentCreatePageTittle": "टूर्नामेंट बनाएं",
            "tournamentCreateHeaderText": "टूर्नामेंट बनाएं",
            "tournamentCreateSubHeaderText": "एक टूर्नामेंट बनाने के लिए मुझे एक टूर्नामेंट का नाम, हर खेल के लिए कितना अधिकतम स्कोर होगा। भूलने से पहले शुभकामनाएं!",
            "tournamentCreateNameText": "टूर्नामेंट का नाम",
            "tournamentCreateMaxPointsText": "अधिकतम स्कोर खेलें",
            "tournamentCreateGameModeText": "खेल मोड",
            "tournamentCreateChooseModeText1": "वनिला",
            "tournamentCreateChooseModeText2": "क्षमताएँ",
            "tournamentCreateButtonCreate": "टूर्नामेंट बनाएं",

            #Joined-Tournament-Room
            "tournamentroomPageTittle": "टूर्नामेंट रूम",
            "tournamentroomHeaderText": "टूर्नामेंट रूम",
            "tournamentroomLeaveButtonText": "छोड़ें",
            "tournamentroomRoomText": "रूम",
            "tournamentroomStartButtonText": "शुरू करें",
            "tournamentroomJoinButtonText": "शामिल हों",
            "tournamentCheckBracketButtonText": "ब्रैकेट देखें",
            "tournamentroomTournamentRoomButton": "टूर्नामेंट रूम",
            "tournamentroomWaitingText": "इंतजार कर",
            "tournamentroomForPlayerText": "खिलाड़ी ",

            #Tournament Room List
            "tournamentRoomListPageTittle": "टूर्नामेंट रूम सूची",
            "tournamentRoomListHeaderText": "टूर्नामेंट रूम सूची",

        #RPS Game
        "rpsGamePageTittle": "रॉक-पेपर-सैंड खेल",
        "rpsGameText1": "रॉक-पेपर-सैंड लॉबी में आपका स्वागत है",
        "rpsGameText2": "आप आर्टिफिशियल इंटेलिजेंस के साथ खेलकर खुद को बेहतर बना सकते हैं। यदि आप किसी वास्तविक व्यक्ति के साथ खेलना चाहते हैं, तो दूसरे विकल्प पर विचार करें; यदि हमें 5 मिनट के भीतर मैच के लिए कोई नहीं मिल सका, तो मैच रद्द कर दिया जाएगा। इससे पहले कि मैं भूल जाऊँ, शुभकामनाएँ!",
        "rpsGameAIButtonText": "ए.आई. के साथ खेलें",
        "rpsGameLocalButtonText": "स्थानीय खेल",
        "rpsGameSearchOpponentButtonText": "विरोधी खोजें ",

        #AI-Game
            "rpsGamePageTittle": "रॉक कागज कैंची आर्टिफिशियल इंटेलिजेंस गेम",
            "rpsGameScoreText": "स्कोर",
            "rpsGameRockText": "पत्थर",
            "rpsGamePaperText": "कागज",
            "rpsGameScissorsText": "कैंची",
            "rpsGamePickedText": "तुमने चुना",
            "rpsGamePickedText2": "विरोधी चुना",
            "rpsGameAgainText": "फिर से खेलें",
            "rpsGameGameOverText": "खेल समाप्त",
            "rpsGameRestartButtonText": "फिर से शुरू करें",
            "rpsGameExitButtonText": "बाहर जाएं",


        #Rankings
        "rankingsPageTittle": "रैंकिंग",
        "rankingsTableRankText": "रैंक",
        "rankingsTableNameText": "नाम",
        "rankingsTableUsernameText": "उपयोगकर्ता नाम",
        "rankingsTableWinsText": "जीतें",
        "rankingsTableLossesText": "हारें",
        "rankingsTableWinRateText": "जीतने की दर",
        "rankingsTablePongPointsText": "पॉन्ग अंक",

        #Store
        "storePageTittle": "दुकान",
        "storeText": "दुकान",
        "storeTagText": "सभी",
        "storeWalletText": "वॉलेट",
        "storeWalleinfoText1": "खेल खेलकर ",
        "storeWalleinfoText2": " जीत सकते हैं।",

        #Inventory
        "inventoryPageTittle": "इन्वेंटरी",
        "inventoryText": "इन्वेंटरी",
        "inventoryTagText": "सभी",
        "inventoryWalletText": "वॉलेट",
        "inventoryWalleinfoText1": "खेल खेलकर ",
        "inventoryWalleinfoText2": " जीत सकते हैं।",
        "inventoryModalHeaderText": "आइटम खरीदें",
        "inventoryModalSaveButton": "खरीदें",
        "inventoryModalCloseButton": "बंद करें",
        "inventoryItemKeyboardInfoText": "उपयोग",
        "inventoryItemKeyboardInfoText2": "इस आइटम के लिए कोई विशेष कीपैड नहीं है, यह स्वचालित रूप से उपयोग किया जाता है।",
        "inventoryItemKeyboardInfoText3": "इस आइटम के लिए कोई विशेष कीपैड नहीं है, यह स्वचालित रूप से उपयोग किया जाता है।",

        
        #Search
        "searchPageTittle": "खोजें",
        "searchInputText": "ईमेल या उपयोगकर्ता नाम या डिस्प्ले नाम खोजें...",
        "searchMessageButtonText": "संदेश",
        "searchFollowButtonText": "अनुसरण करना",
        "searchFollowingButtonText": "करें",
        "searchNoResultFoundText": "कोई परिणाम नहीं मिला।",
        
        #Profile
        "profilePageTittle": "प्रोफ़ाइल",
        "profileRankAIText": "ए.आई. रैंक",
        "profileRankUserText1": " उपयोगकर्ता रैंक",
        "profileRankUserText2": " रैंक",
        "profileFollowButton": "अनुसरण करना",
        "profileFollowingButton": "करें",
        "profileTitleText1": "42 स्कूल समुदाय",
        "profileTitleText2": "पॉन्ग खिलाड़ी",

        "profileMatchHistoryText1": "प्रतिद्वंद्वी",
        "profileMatchHistoryText2": "परिणाम",
        "profileMatchHistoryText3": "अंक",
        "profileMatchHistoryText4": "अवधि",

        "profileMatchHistoryWinText": "जीता",
        "profileMatchHistoryLoseText": "हारा",

        "profileRankText1": "रैंक",

        "profileGameStats1": "खेल खेले गए:",
        "profileGameStats2": "जीतें:",
        "profileGameStats3": "हारें:",
        "profileGameStats4": "जीतने की दर:",
        "profileGameStats5": "औसत अंक जीते:",
        "profileGameStats6": "औसत अंक हारे:",

        #Friends
        "friendsPageTittle": "मित्र",
        "friendsMessageButtonText": "संदेश",
        "friendsNoResultFoundText": "कोई परिणाम नहीं मिला।",


        #ProfileSettings
        "profileSettingsPageTittle": "प्रोफ़ाइल सेटिंग्स",
        "profileSettingsNavbar1": "प्रोफ़ाइल संपादित करें",
        "profileSettingsNavbar2": "पासवर्ड बदलें",
        "profileSettingsNavbar3": "सोशल्स जोड़ें",
        "profileSettingsNavbar4": "अवरुद्ध उपयोगकर्ता",
        "profileSettingsNavbar5": "खाता बंद करें",

        #Edit-Profile
        "editProfileChangeImageText": "छवि बदलें",
        "editProfileUsernameText": "उपयोगकर्ता नाम (आपका नाम साइट पर अन्य उपयोगकर्ताओं के लिए कैसे दिखाई देगा)",
        "editProfileEmailText": "ईमेल",
        "editProfile42EmailText": "चूंकि आप 42 के साथ लॉग इन हैं, आपकी ईमेल सेटिंग सुविधा अक्षम है।",
        "editProfileDisplayNameText": "प्रदर्शन नाम",
        "editProfileSaveButtonText": "परिवर्तन सहेजें",

            #Change-Password
            "changePasswordCurrentPasswordText": "वर्तमान पासवर्ड",
            "changePasswordNewPasswordText": "नया पासवर्ड",
            "changePasswordNewConfirmPasswordText": "नया पासवर्ड पुष्टि करें",
            "changePassword42Text": "चूंकि आप 42 के साथ लॉग इन हैं, आपकी पासवर्ड सेटिंग सुविधा अक्षम है।",
            "changePasswordSaveButtonText": "पासवर्ड सहेजें",

            #Add-Socials
            "addSocialsLinkedinInputText": "अपना LinkedIn उपयोगकर्ता नाम दर्ज करें",
            "addSocialsTwitterInputText": "अपना Twitter उपयोगकर्ता नाम दर्ज करें",
            "addSocialsGithubInputText": "अपना Github उपयोगकर्ता नाम दर्ज करें",
            "addSocialsIntraInputText": "अपना 42 Intra उपयोगकर्ता नाम दर्ज करें",
            "addSocialsSaveButtonText": "सोशल्स सहेजें",

            #Blocked-Users
            "blockedUsersHeaderText": "अवरुद्ध खाते",
            "blockedUsersSubHeaderText": "आप यहां अपने द्वारा अवरुद्ध किए गए खातों को अनवरोधित कर सकते हैं।",
            "blockedStatusText": "अवरुद्ध",

            #Close-Account
            "closeAccountHeaderText": "खाता बंद करें",
            "closeAccountInputText": "ईमेल",
            "closeAccountSubHeaderText": "आप यहां अपना खाता हटा सकते हैं। यह कार्रवाई अपरिवर्तनीय है।",
            "closeAccountButton": "खाता बंद करें",
            
    }
    return context