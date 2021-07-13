## wingman

A python script to create issues on your repo based on comments left in the code

```py
# TODO: Sample todo title
```

For this to work you need to have a github token in your environment variables.
Simply,

```sh
export GITHUB_PERSONAL_TOKEN = token_here
```

or

```ps
$env:GITHUB_PERSONAL_TOKEN = token_here
```

If you want the token to persist across sessions you need to add it to your `.bashrc` or `$PROFILE`.

Inspired by [tsoding/snitch](https://github.com/tsoding/snitch)
