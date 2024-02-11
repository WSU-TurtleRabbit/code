# code

This branch is an attempt to start an initial team behaviour code, with some basic file organisation.

It builds off Eren's code (elsewhere in this repo) for the basic agents, but the idea is to provide a bit more structure and organisation useful for controlling a whole team.

Eventually this should evolve into the more complete team code, with world model etc.

## How to get started

* The initial setup is for grSim, so you will need to install that on your machine:
  https://github.com/RoboCup-SSL/grSim

* Clone this repository / branch on your machine:
  we are using the ssl-vision-client as a submodule, so you should use the "--recursive" option when cloning:

```
  git clone --branch base-team-control --recursive git@github.com:WSU-TurtleRabbit/code.git
```

  If you already cloned the repo, but not recursively, or for a different branch, then you can fix that with these steps:

```
cd code
git checkout base-team-control
git submodule update --init --recursive
```

* Create the `ssl-vision-cli` binary

  This requires node (nodejs and/or npm) and programming language Go to be installed on your machine. Google is your friend.

  If you have that, build the `ssl-vision-cli` binary like this:

```
  cd code/TRControl/ssl-vision-client/cmd/ssl-vision-cli
  go build
```

  This should give you an executable, `ssl-vision-cli` in that directory.

  The executable is also directly available from the ssl-vision-client
  directory and in that case does not need to be build. It will not
  work on every linux version, the above step should work as long as
  you have the required software installed, independent of the linux
  version. If you just download the binary, copy it into your repository, into
  the `code/TRControl/ssl-vision-client/cmd/ssl-vision-cli/` directory.


  

  