# ft_transcendence_newpdf

<p align="center">
    <img src="https://i.hizliresim.com/ctrhatw.png"/>
</p>

## Modules
### Major Modules
<head>
<link rel="stylesheet" href="readme-assets/readme.css">
</head>

<div class="details">
  <details>
      <summary> <b> Standard user management, authentication, users across  tournaments. ⌛</b></summary>
          <ul>
          <li><input type="checkbox" checked disabled/> Users can subscribe to  the website in a secure way. </li>
          <li><input type="checkbox" checked disabled/> Registered users can log  in in a secure way. </li>
          <li><input type="checkbox" checked disabled/> Users can select a  unique display name to play the tournaments. </li>
          <li><input type="checkbox" checked disabled/> Users can update their  information. </li>
          <li><input type="checkbox" checked disabled/> Users can upload an   avatar, with a default option if none is provided. </li>
          <li><input type="checkbox" disabled/> Users can add others as friends   and view their online status. </li>
          <li><input type="checkbox" disabled/> User profiles display stats,  such as wins and losses. </li>
          <li><input type="checkbox" disabled/> Each user has a <b>Match  History</b> including 1v1 games, dates, and relevant
          details, accessible to logged-in users.</li>
          </ul>
          <div class="attention-container">
              <img src="https://cdn.pixabay.com/photo/2013/07/12/14/33/ attention-148478_960_720.png">
              <p class="attention-info">Be carefull, the management of duplicate  usernames/emails is at your discretion. You must provide a   justification for your decision.</p>
          </div>
  </details>
  
  <details>
      <summary> <b>  Implementing a remote authentication. ✅</b></summary>
      In this major module, the goal is to implement the following  authentication system:
      <code>OAuth 2.0 authentication with 42</code>. Key features and objectives  include: <br>
      <b>Be carefull, the management of duplicate usernames/emails is at your
      discretion. You must provide a justification for your decision. </b>
          <ul>
          <li><input type="checkbox" checked disabled/> Integrate the   authentication system, allowing users to securely sign in. </li>
          <li><input type="checkbox" checked disabled/> Obtain the necessary  credentials and permissions from the authority to enable a secure  login. </li>
          <li><input type="checkbox" checked disabled/> Implement user-friendly   login and authorization flows that adhere to best practices and   security standards. </li>
          <li><input type="checkbox" checked disabled/> Ensure the secure   exchange of authentication tokens and user information between the web  application and the authentication provider. </li>
          </ul>
          This major module aims to get a remote user authentication, providing   users with
  a secure and convenient way to access the web application.
  </details>
  
  <details>
      <summary> <b> Remote players ✅</b></summary>
      It is possible to have two distant players. Each player is located on a   separated
  computer, accessing the same website and playing the same Pong game. <br>
  💡 <i>Think about network issues, like unexpected disconnection or lag.
  You have to offer the best user experience possible. </i>
  </details>
  
  <details>
      <summary> <b> Use a Framework as backend. ✅</b></summary>
      In this major module, you are required to utilize a specific web framework  for your backend development, and that framework is <code>Django</code>.   <br>
  <i>You can create a backend without using the constraints of this module
  by using the default language/framework. However, this module will
  only be valid if you use the associated constraints. </i>
  </details>
  
  <details>
      <summary> <b> Live Chat. ⌛</b></summary>
      You have to create a chat for your users in this module:
          <ul>
          <li><input type="checkbox" checked disabled/> The user should be able   to send <b>direct messages</b> to other users. </li>
          <li><input type="checkbox" disabled/> The user should be able to block  other users. This way, they will see no more messages from the account   they blocked. </li>
          <><input type="checkbox" disabled/> The user should be able to  invite other users to play a Pong game through the chat interface. </  li>
          <li><input type="checkbox" disabled/> The tournament system should be   able to warn users expected for the next game. </li>
          <li><input type="checkbox" checked disabled/> The user should be able   to access other players profiles through the chat interface. </li>
          </ul>
  </details>
  
  <details>
      <summary> <b> Introduce an AI Opponent. ⌛</b></summary>
      In this major module, the objective is to incorporate an AI player into   the game. Notably, the use of the <b>A* algorithm</b> is not permitted for  this task. Key features and goals include:
          <ul>
          <li><input type="checkbox" checked disabled/> Develop an AI opponent  that provides a challenging and engaging gameplay experience for   users. </li>
          <li><input type="checkbox" checked disabled/> The AI must replicate   human behavior, meaning that in your AI implementation, you must  simulate keyboard input. The constraint here is that the AI can only   refresh its view of the game once per second, requiring it to   anticipate bounces and other actions. </li>
          <i>The AI must utilize power-ups if you have chosen to implement the  Game customization options module.</i>
          <li><input type="checkbox" disabled/> Implement AI logic and  decision-making processes that enable the AI player to make  intelligent and strategic moves. </li>
          <li><input type="checkbox" checked disabled/> Explore alternative   algorithms and techniques to create an effective AI player without  relying on A*. </li>
          <li><input type="checkbox" disabled/> Ensure that the AI adapts to  different gameplay scenarios and user interactions. </li>
          <div class="attention-container">
              <img src="https://cdn.pixabay.com/photo/2013/07/12/14/33/ attention-148478_960_720.png">
              <p class="attention-info">Attention: You will need to explain in  detail how your AI functions during your evaluation. Creating an   AI that does nothing is strictly prohibited; it must have the   capability to win occasionally.</p>
          </div>
          </br>
          This major module aims to enhance the game by introducing an AI   opponent that adds excitement and competitiveness without relying on  the A* algorithm.
          </ul>
  </details>
  
  <details>
      <> <b> Add Another Game with User History and Matchmaking. ❓</b></  summary>
      In this major module, the objective is to introduce a new game, distinct  from Pong, and incorporate features such as user history tracking and  matchmaking. Key features and goals include:
          <ul>
          <li><input type="checkbox" disabled/> Develop a new, engaging game to   diversify the platform’s offerings and entertain users. </li>
          <li><input type="checkbox" disabled/> Implement user history tracking   to record and display individual user’s gameplay statistics. </li>
          <li><input type="checkbox" disabled/> Create a matchmaking system to  allow users to find opponents and participate in fair and balanced   matches. </li>
          <li><input type="checkbox" disabled/> Ensure that user game history   and matchmaking data are stored securely and remain up-to-date. </li>
          <li><input type="checkbox" disabled/> Optimize the performance and  responsiveness of the new game to provide an enjoyable user  experience. Regularly update and maintain the game to fix bugs, add  new features, and enhance gameplay. </li>
          </ul>
          This major module aims to expand your platform by introducing a new   game, enhancing user engagement with gameplay history, and  facilitating matchmaking for an enjoyable gaming experience.
  </details>
  
  ### Minor Modules
  
  <details>
      <summary> <b> Use a front-end framework or toolkit. ✅</b></summary>
      Your frontend development will utilize the <code>Bootstrap toolkit.</code>  <br>
      <i>You can create a front-end without using the constraints of this module  by using the default language/framework. However, this module will only be   valid if you use the associated constraints.</i>
  </details>
  
  <details>
      <summary> <b> Use a database for the backend -and more. ⌛</b></summary>
      The designated database for all DB instances in your project is   <code>PostgreSQL</code>. This choice guarantees data consistency and  compatibility across all project components and may be a prerequisite for  other modules, such as the <b>backend Framework module</b>.
  </details>
  
  <details>
      <summary> <b> Game Customization Options. ❓</b></summary>
      In this minor module, the goal is to provide customization options for all  available games on the platform. Key features and objectives include:
          <ul>
          <li><input type="checkbox" disabled/> Offer customization features,   such as power-ups, attacks, or different maps, that enhance the   gameplay experience. </li>
          <li><input type="checkbox" disabled/> Allow users to choose a default   version of the game with basic features if they prefer a simpler  experience. </li>
          <li><input type="checkbox" disabled/> Ensure that customization   options are available and applicable to all games offered on the  platform. </li>
          <li><input type="checkbox" disabled/> Implement user-friendly settings  menus or interfaces for adjusting game parameters. </li>
          <li><input type="checkbox" disabled/> Maintain consistency in   customization features across all games to provide a unified user   experience. </li>
          </ul>
          This module aims to give users the flexibility to tailor their gaming   experience across all available games by providing a variety of   customization options while also offering a default version for those   who prefer a straightforward gameplay experience.
  </details>
  
  <details>
      <summary> <b> Support on all devices. ⌛</b></summary>
      In this module, the main focus is to ensure that your website works   seamlessly on all types of devices. Key features and objectives include:
          <ul>
          <li><input type="checkbox" disabled/> Make sure the website is  responsive, adapting to different screen sizes and orientations,   ensuring a consistent user experience on desktops, laptops, tablets,  and smartphones. </li>
          <li><input type="checkbox" disabled/> Ensure that users can easily  navigate and interact with the website using different input methods,  such as touchscreens, keyboards, and mice, depending on the device   they are using. </li>
          </ul>
          This module aims to provide a consistent and user-friendly experience   on all devices, maximizing accessibility and user satisfaction.
  </details>
  
  <details>
      <summary> <b> Expanding Browser Compatibility. ❓</b></summary>
      In this minor module, the objective is to enhance the compatibility of the  web application by adding support for an additional web browser. Key   features and objectives include:
          <ul>
          <li><input type="checkbox" disabled/> Extend browser support to   include an additional web browser, ensuring that users can access and   use the application seamlessly. </li>
          <li><input type="checkbox" disabled/> Conduct thorough testing and  optimization to ensure that the web application functions correctly  and displays correctly in the newly supported browser. </li>
          <><input type="checkbox" disabled/> Address any compatibility issues  or rendering discrepancies that may arise in the added web browser. </ li>
          <li><input type="checkbox" disabled/> Ensure a consistent user  experience across all supported browsers, maintaining usability and  functionality. </li>
          </ul>
          This minor module aims to broaden the accessibility of the web  application by supporting an additional web browser, providing users   with more choices for their browsing experience.
  </details>
  
  <details>
      <summary> <b> Multiple language supports. ❓</b></summary>
      In this minor module, the objective is to ensure that your website  supports multiple languages to cater to a diverse user base. Key features  and goals include:
          <ul>
          <><input type="checkbox" disabled/> Implement support for a minimum   of three languages on the website to accommodate a broad audience. </ li>
          <li><input type="checkbox" disabled/> Provide a language switcher or  selector that allows users to easily change the website’s language   based on their preferences. </li>
          <li><input type="checkbox" disabled/> Translate essential website   content, such as navigation menus, headings, and key information, into  the supported languages. </li>
          <li><input type="checkbox" disabled/> Ensure that users can navigate  and interact with the website seamlessly, regardless of the selected   language. </li>
          <li><input type="checkbox" disabled/> Consider using language packs or  localization libraries to simplify the translation process and   maintain consistency across different languages. </li>
          <li><input type="checkbox" disabled/> Allow users to set their  preferred language as a default choice for subsequent visits to the  website. </li>
          </ul>
          This minor module aims to enhance the accessibility and inclusivity of  your website by offering content in multiple languages, making it more   user-friendly for a diverse international audience.
  </details>
</div>

<div class="user-cards">
  <div class="responsive-container-block container">
      <p class="text-blk team-head-text">
        42 Indian Developers
      </p>
      <div class="responsive-container-block">
        <div class="responsive-cell-block wk-desk-3 wk-ipadp-3 wk-tab-6 wk-mobile-12 card-container">
          <div class="card">
            <div class="team-image-wrapper">
              <img class="team-member-image" src="https://media-ist1-1.cdn.whatsapp.net/v/t61.24694-24/57564842_721317714983120_5899913033106325504_n.jpg?ccb=11-4&   oh=01_AdTh2vxN_PsiGTh_DfCFpc9eybyJaxkXQ-uKLYza-__Jwg&oe=65B6C007&_nc_sid=e6ed6c&_nc_cat=102">
            </div>
            <p class="text-blk name">
              Samet Çiftçi
            </p>
            <p class="text-blk position">
              Django - Backend
            </p>
            <p class="text-blk feature-text">
              👑 Kısaca İmparator 👑
            </p>
            <div class="social-icons">  
              <a href="https://github.com/temasictfic" target="_blank">
                <img width="20" height="20" src="https://img.icons8.com/ios-filled/50/228BE6/github.png" alt="github"/>
              </a>
              <a href="https://x.com/temasictfic" target="_blank">
              <img width="20" height="20" src="https://img.icons8.com/ios-filled/50/228BE6/twitterx--v1.png" alt="twitterx--v1"/>
              </a>
          </div>
        </div>
      </div>
      <div class="responsive-cell-block wk-desk-3 wk-ipadp-3 wk-tab-6 wk-mobile-12 card-container">
        <div class="card">
          <div class="team-image-wrapper">
            <img class="team-member-image" src="https://i.hizliresim.com/ij9ktl2.jpeg">
          </div>
          <p class="text-blk name">
            Furkan Yurtseven
          </p>
          <p class="text-blk position">
            Django - Backend
          </p>
          <p class="text-blk feature-text">
            👑 Jr. İmparator 👑
          </p>
          <div class="social-icons">
            <a href="https://github.com/fyurtsev" target="_blank">
              <img width="20" height="20" src="https://img.icons8.com/ios-filled/50/228BE6/github.png" alt="github"/>
            </a>
            <a href="https://x.com/fyurtsev" target="_blank">
            <img width="20" height="20" src="https://img.icons8.com/ios-filled/50/228BE6/twitterx--v1.png" alt="twitterx--v1"/>
            </a>
          </div>
        </div>
      </div>
      <div class="responsive-cell-block wk-desk-3 wk-ipadp-3 wk-tab-6 wk-mobile-12 card-container">
        <div class="card">
          <div class="team-image-wrapper">
            <img class="team-member-image" src="https://avatars.githubusercontent.com/u/96894640?v=4">
          </div>
          <p class="text-blk name">
            Yunus Emre Aktaş
          </p>
          <p class="text-blk position">
            Joker
          </p>
          <p class="text-blk feature-text">
            👑 Jr. İmparator 👑
          </p>
          <div class="social-icons">
            <a href="https://github.com/temasictfic" target="_blank">
              <img width="20" height="20" src="https://img.icons8.com/ios-filled/50/228BE6/github.png" alt="github"/>
            </a>
            <a href="https://x.com/temasictfic" target="_blank">
            <img width="20" height="20" src="https://img.icons8.com/ios-filled/50/228BE6/twitterx--v1.png" alt="twitterx--v1"/>
            </a>
          </div>
        </div>
      </div>
      <div class="responsive-cell-block wk-desk-3 wk-ipadp-3 wk-tab-6 wk-mobile-12 card-container">
        <div class="card">
          <div class="team-image-wrapper">
            <img class="team-member-image" src="https://avatars.githubusercontent.com/u/66090171?v=4">
          </div>
          <p class="text-blk name">
            Enes Yağız
          </p>
          <p class="text-blk position">
            Frontend
          </p>
          <p class="text-blk feature-text">
            👑 Jr. İmparator 👑
          </p>
          <div class="social-icons">
            <a href="https://github.com/fleizean" target="_blank">
              <img width="20" height="20" src="https://img.icons8.com/ios-filled/50/228BE6/github.png" alt="github"/>
            </a>
            <a href="https://x.com/onlyflei" target="_blank">
            <img width="20" height="20" src="https://img.icons8.com/ios-filled/50/228BE6/twitterx--v1.png" alt="twitterx--v1"/>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>