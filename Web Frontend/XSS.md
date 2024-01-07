# Cross-Site Scripting (XSS) Attacks and Defenses

Cross-site scripting (XSS) is a web security vulnerability that allows attackers to inject malicious client-side scripts into web pages. XSS attacks exploit the trust websites have in users by injecting malicious code into the DOM through improper sanitization of user input. A successful XSS attack can lead to session hijacking, phishing, defacement and more.

There are three main types of XSS attacks:

1. **Reflected XSS**: The malicious script comes from the current HTTP request. The attacker needs to trick the victim into clicking a URL to execute the attack. Reflected XSS can be prevented by sanitizing user input.

    ```
    http://vulnerable.com/search?q=<script>alert(1)</script>
    ```

2. **Stored XSS**: The malicious script comes from the website's database. The script is inserted into the DOM when the page loads. Stored XSS can be prevented by sanitizing user input before storing it in the database.

    ```
    <script>var maliciousCode = '#{storedScript}';</script> 
    ```

3. **DOM-based XSS**: The vulnerability exists in client-side code rather than server-side. The DOM environment can be manipulated to execute injected scripts. DOM XSS can be prevented by sanitizing data before passing it to the DOM.

    ```js
    const userInput = window.location.href.split('=')[1] 
    document.getElementById("message").innerText = userInput;
    ```

## Injection Points

The most common injection points for XSS attacks include:

- **HTML node content**: An attacker can inject scripts into HTML nodes like `div`, `span`, etc.

    ```html
    <div>#{content}</div> 
    ```

  This can be prevented by escaping characters like `<` and `>` with HTML entities.

- **HTML attributes**: Scripts can be injected into tag attributes like `src`, `onerror`, etc.

    ```html
    <img src="#{image}">
    <!-- const image="1\" onerror=\"alert(1)"; -->
    ```

  Attribute values should be sanitized to prevent splitting by quotes.

- **JavaScript code**: User input inserted into JS code can break out of data literals and execute arbitrary code.

```html
<script>
	var data = "#{content}";
	// const content = "hello\";alert(1);";
	var data = "hello";alert(1);"
</script>
```

  Input should be sanitized before interpolating into JS.

- **Rich text editors**: Unfiltered HTML input can lead to XSS if rendered on page. A whitelist approach should be used to filter allowed tags and attributes.

## Defenses

There are several key defenses against XSS attacks:

- **Input validation and escaping**: Special characters like `<`, `>`, `"`, `'` should be escaped on output based on context.
- **Whitelisting**: Only allow specific HTML tags and attributes from rich text input. Disallow inline JS execution.
```javascript
const whitelist = {
	"img": ["src"],
	"font": ["color", "size"],
	"a": ["href"]
};

$("*").each((index, elem) => {
    if (!whitelist[elem.name]) {
        $(elem).remove();
        return;
    }

    for (var attr in elem.attribs) {
        if (whitelist[elem.name].indexOf(attr) === -1) {
            $(elem).attr(attr, null);
        }
    }
});
```
- **Third Party Library**
- **Content Security Policy (CSP)**: An HTTP header that restricts resources the page can load/execute to an allowed list. Can disable unsafe inline/eval.
```
Content-Security-Policy: default-src 'self'; script-src 'nonce-EDNnf03nceIOfn39fn3e9h3sdfa'
```
- **Security headers**: Headers like `X-XSS-Protection` can enable browser XSS filters. But should not be solely relied upon.
- **Sanitization libraries**: Libraries like DOMPurify can sanitize HTML by only allowing whitelisted tags/attributes and disallowing malicious code.

A strong XSS defense requires a combination of the above defenses. The key is to never trust user input and escape/encode output based on context.

## Secure Development Practices

Proper training of developers is critical to avoid common XSS pitfalls:

- Never insert untrusted data into HTML, JS or URLs without sanitization
- Don't rely on blacklisting. Use whitelists for rich text input
- Disable inline JS execution and use CSPs
- Use security headers and escape all output contexts
- Keep frameworks, libraries and dependencies up to date
- Test extensively for XSS vulnerabilities using automation
- Adopt a zero trust approach to user input

A holistic approach to security is required to minimize the risk of XSS. This includes proper developer education, secure coding practices, automated testing and runtime defenses like sanitization and CSPs.
