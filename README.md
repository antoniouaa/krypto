# krypto

A neat little sidekick python script to create issues on your repo based on comments left in the code on your behalf

![Krypto the superdog!](./assets/krypto.jpg)

Convert todo comments in your code

```py
# TODO: Sample todo title
```

to GitHub issues on the repository you're working on!
![Sample issue on Github](./assets/issueOnGithub.png)

---

## Env Variables

For this to work you need to have a github token in your environment variables.
To acquire a token navigate to [Developer Settings](https://github.com/settings/tokens) and generate one.

With the token in hand, simply,

```sh
export GITHUB_PERSONAL_TOKEN = token_here
```

or

```ps
$env:GITHUB_PERSONAL_TOKEN = token_here
```

If you want the token to persist across sessions you need to add it to your `.bashrc` or `$PROFILE`.

---

Inspired by [tsoding/snitch](https://github.com/tsoding/snitch)
