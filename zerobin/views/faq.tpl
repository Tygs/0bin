<div class="well" id="faq">

   <h1>FAQ</h1>

      <p></p>

      <h4>How does 0bin work?</h4>

         <p>A random key is generated and used to encrypt the paste, thanks to
            the <a href="http://crypto.stanford.edu/sjcl/">sjcl</a>
            JavaScript library.</p>
         <p>The encrypted content is then sent to the server, which returns the
            address of the newly created paste.</p>
         <p>The JavaScript code redirects to this address, but it adds the
            encryption key in the URL hash (#).</p>
         <p>When somebody wants to read the paste, they will usually click on a link
            with this URL. If the hash containing the key is a part of it, 0bin's
            JavaScript will use it to decrypt the content sent by the server.</p>
         <p>The browser never sends the hash to the server, so the latter does not
            receives the key at any time.</p>


      <h4>But JavaScript encryption is not secure!</h4>

         <p>No, it isn't.</p>
         <p>The goal of 0bin is <strong>not</strong> to protect the user and their data
            (including, obviously, their secrets).</p>
         <p>Instead, it aims to protect the host from being sued for the
            content users pasted on the pastebin. The idea is that you cannot
            require somebody to moderate something they cannot read - as such,
            the host is granted plausible deniability.</p>

         <p>Remember that as an user, you should use 0bin in the same way as unencrypted and
            insecure pastebins - that is, with caution. The only difference with those is that if
            you decide to host a 0bin server, the encryption feature hopefully be used as a defense.
            This is not proven, though! :-)</p>


      <h4>What if the server changes the JavaScript code? And what happens in the case of a <a
            href="https://en.wikipedia.org/wiki/Man-in-the-middle_attack">MITM attack</a>?</h4>

         <p>Read above.</p>
         <p>0bin is not built, and does not aim, to protect user data - but rather the host.
            If any user data is compromised, 0bin still provides the host with
            plausible deniability (as they ignore the content of the pastes).</p>
         <p>It would make no sense if the host was to compromise the encryption process
            to read the data; in that case, they wouldn't have
            installed 0bin in the first place, as 0bin is here to protect them.</p>
         <p><strong>However, if you want to ensure your data is not read in anyway, you should
               not use 0bin</strong>. Use <a href="http://www.cypherpunks.ca/otr/">OTR</a> for chatting,
            <a href="https://gnupg.org/">GnuPG</a> for encrypted & verified data sharing, with <a
               href="https://www.enigmail.net/">EnigMail</a>
            for emails.</p>
         <p>It would be unlikely for those softwares to fail you. Errors will nearly always come from your side - you
            ought to have a perfect <a href="https://en.wikipedia.org/wiki/Operations_security">operations security</a>
            if you do not want your data to be leaked. Remember to use your common sense.</p>

      <h4>How did the idea of 0bin emerge?</h4>

         <p>0bin is based on <a href="http://sebsauvage.net/wiki/doku.php?id=php:zerobin">sebsauvage's work</a>.
            The project sprang as a reaction to <a
               href="https://www.zdnet.com/blog/security/pastebin-to-hunt-for-hacker-pastes-anonymous-cries-censorship/11336">the
               implementation of a moderation system on Pastebin</a>,
            due to the significant amount of illegal content pasted on it, or that it linked to.</p>

      <h4>How can I get 0bin?</h4>

         <p>0bin is an open-source project, and the code is hosted on <a
               href="https://github.com/sametmax/0bin">GitHub</a>.
            You can either download a tarball or clone the repository.</p>

</div>


% rebase("base", settings=settings, pastes_count=pastes_count)
