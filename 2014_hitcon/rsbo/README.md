rsbo
======

Files usage:

To run a local copy the file /home/rsbo/flag must exist, put some text in it this is the flag.
To run the service locally enter the following:

```
$ mkfifo pipe
$ nc -l 127.0.0.1 4444 < pipe | stdbuf -i0 -o0 -e0 ./rsbo.bin > pipe
```

To exploit it and read the flag enter this:

`python solver.py 127.0.0.1 4444`
