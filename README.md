<!-- ![Krypto the superdog!](./assets/krypto.jpg) -->
<!-- ![usage of krypto](./assets/sample-use.gif) -->

<div align="center">
    <img src="./assets/krypto.jpg"  style="border-radius: 10%;">
    <h2 style="font-size: 48px">Krypto</h2>

![tests](https://github.com/antoniouaa/krypto/actions/workflows/test.yml/badge.svg)
![black](https://github.com/antoniouaa/krypto/actions/workflows/black.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<h2 style="font-size: 22px;">A neat little sidekick python script to create issues on your repo based on comments left in the code on your behalf</h2>

</div>

<div align="center">
    <img src="./assets/sample-use.gif"/>
</div>
Convert todo comments in your code

```py
# TODO: Make config file
# Sometimes you might wanna have TODOs in your tests.
# Right now krypto will completely ignore any file with the
# substring "test" in the path. I would want to be able to
# configure this behaviour.
```

to GitHub issues on the repository you're working on!

![Sample issue on Github](./assets/issue-on-github.png)

---

## Env Variables

For this to work you need to have a github token in your environment variables.
To acquire a token navigate to [Developer Settings](https://github.com/settings/tokens) and generate one.

With the token in hand, simply,

```sh
export TOKEN_GITHUB = token_here
```

or

```ps
$env:TOKEN_GITHUB = token_here
```

If you want the token to persist across sessions you need to add it to your `.bashrc` or `$PROFILE`.

---

Inspired by [tsoding/snitch](https://github.com/tsoding/snitch)
