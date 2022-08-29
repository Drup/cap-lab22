Remote work on ENSL machines

# SSH on ENSL machines, Linux version (with your ENSL Account)


* Edit your `.ssh/config` and add the following lines:
```
Host !ssh.ens-lyon.fr *.ens-lyon.fr
ProxyCommand ssh -N -W %h:%p %r@ssh.ens-lyon.fr
```

* now `ssh` on one of the ENSL machines: 

```
ssh mylogin@slsu0-02.dsi-ext.ens-lyon.fr
```
(`slsu0` or `slsu1`, `01` to `20` at least, use `-X` if you want to use a graphical interface remotely).


# Windows version.

* adapt the `mobaxterm` howto from [this page](https://nlouvet.gitlabpages.inria.fr/lifasr5/connec.html) The ssh gateway is `ssh.ens-lyon.fr` and the machine to log on is `slsu[0-1]-...` 

# Mount your ENS account on your laptop (Linux) with SSHFS. 

* I give you in `scripts/mountsinfoens` a script I wrote many years ago, use with caution.

# Remote debugging with tmux

`tmux` is a terminal multiplexer, that is you can transform one session into
many virtual sessions. Here we are using it to share one session between
multiple users so that we can help you debug in real time on your machine.

Follow the following steps to share a tmux session with another user (this
method is not really secure and should not be used anywhere else):

  - Connect a tmux session with a sensible name (ie. your id) in a shared directory (ie. /tmp):
    `tmux -S /tmp/<yourid>`
  - Allow the socket to be read by others:
    `chmod 777 /tmp/<yourid>`
  - Give us the name of the socket (`/tmp/<yourid>`) so that we can connect to
    your session with the command `tmux -S /tmp/<yourid> attach`

Inside your terminal session, you can use your favorite terminal editor, for
example `vim`, `emacs -nw`, `kak`, `nano` or whatever you like.

Quick overview of tmux:
  -  C-b c     : create a new window
  -  C-b n/p   : go to next/previous window
  -  C-b d     : detach current client
  -  C-b [0-9] : go to window [0-9]
  -  C-b "     : split horizontally
  -  C-b %     : split vertically
  -  C-b up    : go up (same for down, left, right, etc), you can use ijkl

