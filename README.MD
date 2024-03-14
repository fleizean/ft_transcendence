# ft_transcendence_newpdf*

<p align="center">
    <img src="https://i.hizliresim.com/ctrhatw.png"/>
</p>



## Mandatory part

<details>
      <summary> <b> Minimal technical requirement ⌛</b></summary>
          <ul>
          <li>✅ The frontend should be developed using pure vanilla <b>Javascript.</b> </li>
          <li>⌛ Your website must be a <b>single-page application.</b> The user should be able to use the
<b>Back</b> and <b>Forward</b> buttons of the browser. </li>
          <li>✅ Your website must be compatible with the latest stable up-to-date version of
Google Chrome . </li>
          <li>⌛ The user should encounter no unhandled errors and no warnings when browsing the
website. </li>
          <li>⌛ Everything must be launched with a single command line to run an autonomous
container provided by Docker. Example : docker-compose up --build </li>
          </ul>
</details>

<details>
      <summary> <b> Game ⌛</b></summary>
      The main purpose of this website is to play Pong versus other players.
          <ul>
          <li>✅ Therefore, users must have the ability to participate in a live Pong game against
another player directly on the website. Both players will use the same keyboard.
The <b>Remote players module</b> can enhance this functionality with remote players.</li>
          <li>⌛ A player must be able to play against another player, but it should also be possible
to propose a <b>tournament.</b> This tournament will consist of multiple players who
can take turns playing against each other. You have flexibility in how you implement
the tournament, but it must clearly display who is playing against whom and the
order of the players. </li>
          <li>✅ A <b>registration system</b> is required: at the start of a tournament, each player
must input their alias name. The aliases will be reset when a new tournament
begins. However, this requirement can be modified using the <b>Standard User
Management module.</b> </li>
          <li>⌛ There must be a <b>matchmaking system:</b> the tournament system organize the
matchmaking of the participants, and announce the next fight. </li>
          <li>✅ All players must adhere to the same rules, which includes having identical paddle
speed. This requirement also applies when using AI; the AI must exhibit the same
speed as a regular player. </li>
          <li>✅ The game itself must be developed in accordance with the default frontend con-
straints (as outlined above), or you may choose to utilize the <b>FrontEnd module</b>,
or you have the option to override it with the <b>Graphics module.</b> While the visual
aesthetics can vary, it must still capture the essence of the <b>original Pong</b> (1972). </li>
          </ul>
</details>

<details>
      <summary> <b> Security concerns ⌛</b></summary>
          <ul>
          <li>✅ Any password stored in your database, if applicable, must be <b>hashed.</b> </li>
          <li>✅ Your website must be protected against <b>SQL injections/XSS.</b> </li>
          <li>⌛ If you have a backend or any other features, it is mandatory to enable an HTTPS
connection for all aspects (Utilize wss instead of ws...). </li>
          <li>✅ You must implement some form of validation for forms and any user input, either
within the base page if no backend is used or on the server side if a backend is
employed. </li>
          </ul>
          <b>Please make sure you use a strong password hashing algorithm.</b><br>
<b>For obvious security reasons, any credentials, API keys, env
variables etc... must be saved locally in a .env file and ignored by
git. Publicly stored credentials will lead you directly to a failure
of the project.</b>
</details>

## Modules
### Major Modules

  <details>
      <summary> <b> Standard user management, authentication, users across  tournaments. ✅</b></summary>
          <ul>
          <li>✅ Users can subscribe to  the website in a secure way. </li>
          <li>✅ Registered users can log  in in a secure way. </li>
          <li>✅ Users can select a  unique display name to play the tournaments. </li>
          <li>✅ Users can update their  information. </li>
          <li>✅ Users can upload an   avatar, with a default option if none is provided. </li>
          <li>✅ Users can add others as friends   and view their online status. </li>
          <li>✅ User profiles display stats,  such as wins and losses. </li>
          <li>✅ Each user has a <b>Match  History</b> including 1v1 games, dates, and relevant
          details, accessible to logged-in users.</li>
          </ul>
  </details>
  
  <details>
      <summary> <b>  Implementing a remote authentication. ✅</b></summary>
      In this major module, the goal is to implement the following  authentication system:
      <code>OAuth 2.0 authentication with 42</code>. Key features and objectives  include: <br>
      <b>Be carefull, the management of duplicate usernames/emails is at your
      discretion. You must provide a justification for your decision. </b>
          <ul>
          <li>✅ Integrate the   authentication system, allowing users to securely sign in. </li>
          <li>✅ Obtain the necessary  credentials and permissions from the authority to enable a secure  login. </li>
          <li>✅ Implement user-friendly   login and authorization flows that adhere to best practices and   security standards. </li>
          <li>✅ Ensure the secure   exchange of authentication tokens and user information between the web  application and the authentication provider. </li>
          </ul>
          This major module aims to get a remote user authentication, providing   users with
  a secure and convenient way to access the web application.
  </details>
  
  <details>
      <summary> <b> Remote players ⌛</b></summary>
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
          <li>⌛ The user should be able   to send <b>direct messages</b> to other users. </li>
          <li>⌛ The user should be able to block  other users. This way, they will see no more messages from the account   they blocked. </li>
          <li>⌛ The user should be able to  invite other users to play a Pong game through the chat interface. </li>
          <li>⌛ The tournament system should be   able to warn users expected for the next game. </li>
          <li>⌛ The user should be able   to access other players profiles through the chat interface. </li>
          </ul>
  </details>
  
  <details>
      <summary> <b> Introduce an AI Opponent. ✅</b></summary>
      In this major module, the objective is to incorporate an AI player into   the game. Notably, the use of the <b>A* algorithm</b> is not permitted for  this task. Key features and goals include:
          <ul>
          <li>✅ Develop an AI opponent  that provides a challenging and engaging gameplay experience for   users. </li>
          <li>✅ The AI must replicate   human behavior, meaning that in your AI implementation, you must  simulate keyboard input. The constraint here is that the AI can only   refresh its view of the game once per second, requiring it to   anticipate bounces and other actions. </li>
          <li>✅ The AI must utilize power-ups if you have chosen to implement the  Game customization options module.</li>
          <li>✅ Implement AI logic and  decision-making processes that enable the AI player to make  intelligent and strategic moves. </li>
          <li>✅ Explore alternative   algorithms and techniques to create an effective AI player without  relying on A*. </li>
          <li>✅ Ensure that the AI adapts to  different gameplay scenarios and user interactions. </li>
          </br>
          <b>This major module aims to enhance the game by introducing an AI   opponent that adds excitement and competitiveness without relying on  the A* algorithm.</b>
          </ul>
  </details>
  
  <details>
      <summary> <b> Add Another Game with User History and Matchmaking. ❓</b></summary>
      In this major module, the objective is to introduce a new game, distinct  from Pong, and incorporate features such as user history tracking and  matchmaking. Key features and goals include:
          <ul>
          <li>✅ Develop a new, engaging game to   diversify the platform’s offerings and entertain users. </li>
          <li>✅ Implement user history tracking   to record and display individual user’s gameplay statistics. </li>
          <li>❓ Create a matchmaking system to  allow users to find opponents and participate in fair and balanced   matches. </li>
          <li>✅ Ensure that user game history   and matchmaking data are stored securely and remain up-to-date. </li>
          <li>✅ Optimize the performance and  responsiveness of the new game to provide an enjoyable user  experience. Regularly update and maintain the game to fix bugs, add  new features, and enhance gameplay. </li>
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
      <summary> <b> Use a database for the backend -and more. ✅</b></summary>
      The designated database for all DB instances in your project is   <code>PostgreSQL</code>. This choice guarantees data consistency and  compatibility across all project components and may be a prerequisite for  other modules, such as the <b>backend Framework module</b>.
  </details>
  
  <details>
      <summary> <b> Game Customization Options. ✅</b></summary>
      In this minor module, the goal is to provide customization options for all  available games on the platform. Key features and objectives include:
          <ul>
          <li>✅ Offer customization features,   such as power-ups, attacks, or different maps, that enhance the   gameplay experience. </li>
          <li>✅ Allow users to choose a default   version of the game with basic features if they prefer a simpler  experience. </li>
          <li>✅ Ensure that customization   options are available and applicable to all games offered on the  platform. </li>
          <li>✅ Implement user-friendly settings  menus or interfaces for adjusting game parameters. </li>
          <li>✅ Maintain consistency in   customization features across all games to provide a unified user   experience. </li>
          </ul>
          This module aims to give users the flexibility to tailor their gaming   experience across all available games by providing a variety of   customization options while also offering a default version for those   who prefer a straightforward gameplay experience.
  </details>
  
  <details>
      <summary> <b> Support on all devices. ❌</b></summary>
      In this module, the main focus is to ensure that your website works   seamlessly on all types of devices. Key features and objectives include:
          <ul>
          <li>✅ Make sure the website is  responsive, adapting to different screen sizes and orientations,   ensuring a consistent user experience on desktops, laptops, tablets,  and smartphones. </li>
          <li>❌ Ensure that users can easily  navigate and interact with the website using different input methods,  such as touchscreens, keyboards, and mice, depending on the device   they are using. </li>
          </ul>
          This module aims to provide a consistent and user-friendly experience   on all devices, maximizing accessibility and user satisfaction.
  </details>
  
  <details>
      <summary> <b> Expanding Browser Compatibility. ❓</b></summary>
      In this minor module, the objective is to enhance the compatibility of the  web application by adding support for an additional web browser. Key   features and objectives include:
          <ul>
          <li>❓ Extend browser support to   include an additional web browser, ensuring that users can access and   use the application seamlessly. </li>
          <li>❓ Conduct thorough testing and  optimization to ensure that the web application functions correctly  and displays correctly in the newly supported browser. </li>
          <li>❓ Address any compatibility issues  or rendering discrepancies that may arise in the added web browser. </li>
          <li>❓ Ensure a consistent user  experience across all supported browsers, maintaining usability and  functionality. </li>
          </ul>
          This minor module aims to broaden the accessibility of the web  application by supporting an additional web browser, providing users   with more choices for their browsing experience.
  </details>
  
  <details>
      <summary> <b> Multiple language supports. ✅</b></summary>
      In this minor module, the objective is to ensure that your website  supports multiple languages to cater to a diverse user base. Key features  and goals include:
          <ul>
          <li>✅ Implement support for a minimum   of three languages on the website to accommodate a broad audience. </li>
          <li>✅ Provide a language switcher or  selector that allows users to easily change the website’s language   based on their preferences. </li>
          <li>✅ Translate essential website   content, such as navigation menus, headings, and key information, into  the supported languages. </li>
          <li>✅ Ensure that users can navigate  and interact with the website seamlessly, regardless of the selected   language. </li>
          <li>✅ Consider using language packs or  localization libraries to simplify the translation process and   maintain consistency across different languages. </li>
          <li>✅ Allow users to set their  preferred language as a default choice for subsequent visits to the  website. </li>
          </ul>
          This minor module aims to enhance the accessibility and inclusivity of  your website by offering content in multiple languages, making it more   user-friendly for a diverse international audience.
  </details>


<hr>
<br>
<br>
<center>
<h1> Our Team - indian full stack developers 🇮🇳</h1>

<table class="ourteam">
  <tr>
    <td align="center"><a href="https://github.com/temasictfic/" style="text-decoration:none; color: #00ff15;"><img src="https://i.hizliresim.com/mu0ink4.jpg" width="100px;" alt=""/><br /><sub><b>sciftci (Samet)</b></sub></a><br />
    <br><a href="https://profile.intra.42.fr/users/sciftci" title="Intra 42"><img src="https://img.shields.io/badge/Kocaeli-FFFFFF?style=plastic&logo=42&logoColor=000000" alt="Intra 42"/></a></td>
    <td align="center"><a href="https://github.com/fyurtsev/" style="text-decoration:none; color: #00ff15;"><img src="https://i.hizliresim.com/ij9ktl2.jpeg" width="100px;" alt=""/><br /><sub><b>fyurtsev (Furkan)</b></sub></a><br /><br>
    <a href="https://profile.intra.42.fr/users/fyurtsev" title="Intra 42"><img src="https://img.shields.io/badge/Kocaeli-FFFFFF?style=plastic&logo=42&logoColor=000000" alt="Intra 42"/></a></td>
    <td align="center"><a href="https://github.com/yeaktas/" style="text-decoration:none; color: #00ff15;"><img src="https://avatars.githubusercontent.com/u/96894640?v=4" width="100px;" alt=""/><br /><sub><b>yaktas (Yunus Emre)</b></sub></a><br /><br>
    <a href="https://profile.intra.42.fr/users/yaktas" title="Intra 42"><img src="https://img.shields.io/badge/Kocaeli-FFFFFF?style=plastic&logo=42&logoColor=000000" alt="Intra 42"/></a></td>
    <td align="center"><a href="https://github.com/cantaskin/" style="text-decoration:none; color: #00ff15;"><img src="https://avatars.githubusercontent.com/u/94763376?v=4" width="100px;" alt=""/><br /><sub><b>ataskin (Can) </b></sub></a><br /><br>
    <a href="https://profile.intra.42.fr/users/ataskin" title="Intra 42"><img src="https://img.shields.io/badge/Kocaeli-FFFFFF?style=plastic&logo=42&logoColor=000000" alt="Intra 42"/></a></td>
    <td align="center"><a href="https://github.com/fleizean/" style="text-decoration:none; color: #00ff15;"><img src="https://avatars.githubusercontent.com/u/66090171?v=4" width="100px;" alt=""/><br /><sub><b>eyagiz (Enes)</b></sub></a><br /><br>
    <a href="https://profile.intra.42.fr/users/eyagiz" title="Intra 42"><img src="https://img.shields.io/badge/Kocaeli-FFFFFF?style=plastic&logo=42&logoColor=000000" alt="Intra 42"/></a></td>
  </tr>
</table>
</center>

