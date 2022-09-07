# Private-Net.work site

<p align="center">
  <a href="https://private-net.work">
  <img src="https://private-net.work/static/img/thumb.jpeg" alt="Private-Net.work">
  </a>
</p>
<p align="center">
    <em>Private-Net.work is a service, that will help you hide the most private data from 
    being read by third parties when sharing it with one interlocutor. 
    Instead of sharing your passwords, payment details, addresses and 
    other confidential data in the clear in messengers, 
    send your partner a link to the one-time note generated by 
    <a href="https://private-net.work" target="_blank">our website</a>.</em>
</p>
<p align="center">
<a href="https://stats.uptimerobot.com/YnWpPiD9Lo" target="_blank">
    <img src="https://img.shields.io/uptimerobot/ratio/m791547864-87556c1a8d4f6cc3c14b8a6b" alt="Uptime">
</a>
<a href="https://github.com/Private-Net-work/Private-Net.work-site/actions/workflows/pylint.yml" target="_blank">
    <img src="https://img.shields.io/github/workflow/status/Private-Net-work/Private-Net.work-site/Pylint?label=Pylint" alt="Pylint">
</a>
<a href="https://private-net.work?lang=en" target="_blank">
    <img src="https://img.shields.io/badge/English-translated%20-lightgrey" alt="English translated">
</a>
<a href="https://private-net.work?lang=ru" target="_blank">
    <img src="https://img.shields.io/badge/Русский-переведён%20-lightgrey" alt="Русский переведён">
</a>
</p>

---

In this repository you can see the source code for our site 
<a href="https://private-net.work" target="_blank">private-net.work</a>.
Our mission is to stand for privacy in messaging services. The mentioned above 
site helps users share confidential data privately without being read by 
third parties.

## How to use

#### Alice

The process of sending data is very simple. Alice can make a disposable note 
with text or a document on the main page. The note's content is securely 
encrypted by your browser with AES (CTR) cipher and sent to our server. We put this 
encrypted note to our database without any unnecessary metadata and show Alice the 
link, which is shortened by our partner service. She can send this link 
in any chat.

#### Bob

After Bob gets the link, he opens it in his browser. 
When he agrees to open the note we will send him encrypted content. 
His browser will decrypt the note using the anchor, 
that was put by Alice's browser in the link. When the note is encrypted he would 
be able to see it's content on the screen. In case he was sent a document he 
would be able to download it. We don't save the document's title, but we try to
store its extension. Sometimes it's better to notify 
receiver about the true extension.

#### David (Third party)

<p>Let's imagine, that David will steal Bob's password and get access to all his 
chats. He'll find the link, that Alice sent Bob. But after opening it he'll 
see a 404 page of our partner shortener. He won't even know, that it was a link 
to the note! That's because all our notes are completely deleted from our database
after first been read. They are also been deleted after 7 days from being sent 
or even earlier, if Alice decided to set a custom period of time.</p>

<p>If David will be faster to read the note than Bob, he would be able to do it. 
But when Bob will get a 404 error he would know that there were unwanted visitors 
in his chat.</p>

---

**Important!** _All notes are deleted after the first reading! 
If you will forget to save important data the only solution 
will be to ask the sender create a new note._

---

## How to start this application

Our site is actually a Flask application. To start a development server you can 
just run `app.py`.

## License

This project is licensed under the terms of the MIT license.
