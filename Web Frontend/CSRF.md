# CSRF
> Cross Site Reuqest Forgery(跨站请求伪造)
> (CSRF) is a web vulnerability that allows attackers to perform unauthorized actions on a web application in an authorized user's context. It exploits the browser's same-origin policy and the inherent trust websites have in authenticated users' session cookies. Through various techniques, CSRF tricks users into inadvertently loading malicious requests originating from the attacker's website, but attributed to the victim's authenticated session.

## CSRF Attack Anatomy
In a CSRF attack, the victim first authenticates to the vulnerable target web application, which establishes a trusted session cookie. The victim then visits, views or interacts with a separate attacker-controlled site. This could be through an email link, instant message, posting, advertisement or other medium.

The attacker's site contains a crafted `URL` or `hidden HTML` that triggers a forged request to the target site to perform an action as the victim. As the victim is still authenticated to the target, this request will carry the user's session cookie and appear valid. Typical actions include **funds transfers**, **changing account details**, **content deletion** and **privilege escalation**.

### Submitting a form that posts to the target site - The form is submitted via JavaScript without any visible UI using the victim's cookies.(`one click attack`)
the attacker may use such a hidden `iframe` to perform a series of operations in the name of the current user.

If the `target` of `form` is the `name` of an `iframe`, the form will be submitted and jumped in the `iframe` page. But the `display` of `iframe` is `none`, so this process is invisible to the user.
```html
<body>
<script>
    document.write(`
    <form name="commentForm" target="iframe_name" method="post" action="http://bankserver/post/transferMoney">
        <input name="postId" type="hidden" value="stevenyin" />
        <textarea name="amount">10000</textarea>
    </form>
    `);
    var iframe = doc  ument.createElement('iframe');
    iframe.name = 'iframe_name';
    iframe.style.display = 'none';
    document.body.appendChild(iframe);
    setTimeout(function() {
        document.querySelector('[name=commentForm]').submit();
    }, 1000);
</script>
</body>
```
### Persuading the victim to click a crafted link - The link navigates the victim to the target site with a malicious payload in parameters.
```html
<body>
<a href="http://bankserver/transfer?clientId=111&amount=10000&description=stupidDesign">
    Click me to get money!
</a>
</body>
```
As long as the user clicks on this link, a get request will be sent to the server through a `GET` request.


### Loading a page with a malicious image URL - The image tag src attribute triggers a GET request to the target site, which means you even don't need to click any buttons, the GET request will be triggered automatically.
```html
<body>
<img src="http://bankserver/transfer?clientId=111&amount=10000&description=stupidDesign" />
</body>
```

### Stored XSS to inject a CSRF payload - Stored scripts can inject forms or links that trigger automatically for other users.
```html
<body>
<img src="http://bankserver/addComment?comment=<a href='https://some.phishing.websites/click_and_delete_all_your_data_!'>Click me!</a>" />
</body>
```

## The impact of a CSRF attack depends on the function of the targeted application and privileges of the victim's session. Some potential impacts include:
- Financial - Transferring funds, trading stocks, money laundering.
- Account Takeover - Changing account email, password, privileges.
- Data Loss - Deleting content, posts or messages.
- Reputation Damage - Posting offensive content as a user.
- Service Abuse - Sending spam, DDOS participation.
- Session Hijacking - Stealing session cookies via scripts.


## CSRF Attack Defense Mechanisms
> To prevent CSRF attacks, state changing requests must be verified to originate from the site's authorized UI flows, not cross-origin requests.
### CSRF Attack Mechanisms
1. Victim signed in the `WEBSITE A`
2. `WEBSITE A` authenticated the victim and save user's `session` via `cookies.`
3. `WEBSITE EVIL` used a crafted URL or hidden HTML, pretends to be a `user` to access `WEBSITE A`.

### Key points during CSRF
1. `WEBSITE EVIL` sends requests to `WEBSITE A`.
2. `WEBSITE EVIL` carries  `WEBSITE A`'s `Cookie`.
3. This request was not initiated from `WEBSITE A`'s page, but from `WEBSITE EVIL`'s page
4. `http headers`'s `referer` contains the `URL` of `WEBSITE EVIL`

### Preventing CSRF Vulnerabilities
> To prevent CSRF attacks, state changing actions must verify the request originated from the real UI flow, not a cross-origin call.
#### CSRF Tokens
Generate randomized, unique tokens that are required to be submitted with state changing requests. The server validates the token which thwarts forged requests.
- Verify tokens match on both client and server side.
- Bind tokens to the user session with server side storage.
- Rotate CSRF tokens during authentication state change. 
#### SameSite Cookie Attribute
Cookies can be configured with a SameSite attribute that prevents the browser from sending them in cross-origin requests from third party sites.

- Set SameSite to Lax or Strict depending on site functionality.
- Falls back to CSRF tokens if SameSite not **supported** by browser.

#### Referer Header Check
The Referer header indicates the source site of a request. Checking that the Referer comes from your own origin can prevent CSRF.

- However, Referer can be spoofed or not sent at all.
- Should not be only line of defense.

#### Re-authentication for Sensitive Actions
Require users re-enter credentials for high risk state changes like account recovery, password change, etc. This adds user interaction to the flow.

#### CAPTCHA
Challenge–response tests like CAPTCHA prompt user interaction before high risk actions. This prevents automated CSRF exploits.

### Secondary CSRF Defenses
Additional measures to minimize attack surface:

- Avoid `GET` requests for state changes - Use `POST` which cannot be forged `cross-origin`.
- Sanitize rich text editors - Prevent `XSS` flaws which could inject `CSRF` payloads.
- Rotate session identifier with auth changes - Prevents session fixation.
- Limit credentials in `CORS` requests - Set withCredentials false where not needed.
- Temporary identifier binding - Bind user action to temp ID to prevent reuse.
