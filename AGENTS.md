# Repository instructions

## Git network access

Run network Git commands directly, without a proxy. This applies to `git push`,
`git pull`, `git fetch`, `git clone`, `git ls-remote`, and submodule operations
that access the network.

Use this command pattern, replacing `<command> [args...]` with the requested Git
operation:

```sh
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY \
    -u http_proxy -u https_proxy -u all_proxy \
    -u GIT_PROXY_COMMAND -u GIT_SSH -u GIT_SSH_COMMAND \
    NO_PROXY='*' no_proxy='*' \
    git -c http.proxy= -c remote.origin.proxy= \
        -c core.sshCommand='ssh -o ProxyCommand=none -o ProxyJump=none' \
        <command> [args...]
```

For a remote other than `origin`, also set `-c remote.<name>.proxy=` for that
remote. Keep SSH host-key verification enabled. Do not change global proxy,
Git, or SSH settings. If direct access fails, report the network error rather
than falling back to a proxy.
